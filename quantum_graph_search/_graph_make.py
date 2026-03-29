"""Graph-construction utilities that return dense adjacency matrices."""

import numpy as np
from scipy.linalg import block_diag

from quantum_graph_search._graph_attributes import is_connected
from quantum_graph_search._validation import require_int, require_probability


def _require_int(name, value, minimum=None):
    """
    Validate integer-valued constructor arguments.
    """

    return require_int(name, value, minimum=minimum)


def _require_probability(name, value):
    """
    Validate edge probabilities.
    """

    return require_probability(name, value)


def _sample_symmetric_block(size, probability):
    """
    Sample an undirected Erdos-Renyi block of the requested size.
    """

    block = np.zeros((size, size))
    triu_ind = np.triu_indices(size, k=1)
    block[triu_ind] = np.random.binomial(1, probability, len(triu_ind[0]))
    block[(triu_ind[1], triu_ind[0])] = block[triu_ind]
    return block


def complete(g_size):
    """
    Return the adjacency matrix of a complete graph of the given size.
    """

    g_size = _require_int("g_size", g_size, minimum=1)
    adj = np.ones((g_size, g_size))
    np.fill_diagonal(adj, 0)
    return adj


def tree(g_size):
    """
    Randomly generate a tree with ``g_size`` nodes.
    """

    g_size = _require_int("g_size", g_size, minimum=1)
    if g_size == 1:
        return np.zeros((1, 1))

    adj = np.array([[0, 1], [1, 0]])

    for _ in range(2, g_size):
        augment = np.zeros((len(adj), 1))
        link_to = np.random.randint(0, len(adj))
        augment[link_to, 0] = 1
        adj = np.block([[adj, augment], [augment.T, 0]])
    return adj


def cycle(graph_size, num_spikes):
    """
    Produce an undirected cycle graph with optional spikes.
    """

    graph_size = _require_int("graph_size", graph_size, minimum=3)
    num_spikes = _require_int("num_spikes", num_spikes, minimum=0)
    cycle_size = graph_size - num_spikes
    if cycle_size < 3:
        raise ValueError("graph_size - num_spikes must be at least 3")

    adj = np.roll(np.eye(cycle_size), -1) + np.roll(np.eye(cycle_size), 1)
    np.fill_diagonal(adj, 0)
    adj[-1, 0], adj[0, -1] = 1, 1

    adj = block_diag(adj, np.zeros((num_spikes, num_spikes)))
    if num_spikes == 0:
        return adj

    spike_at = np.random.randint(0, cycle_size, num_spikes)
    for k in range(num_spikes):
        adj[-k - 1, spike_at[k]], adj[spike_at[k], -k - 1] = 1, 1

    return adj


def barabasi(graph_size, m_0):
    """
    Generate a graph with the Barabasi-Albert model.
    """

    graph_size = _require_int("graph_size", graph_size, minimum=2)
    m_0 = _require_int("m_0", m_0, minimum=2)
    if m_0 > graph_size:
        raise ValueError("m_0 cannot exceed graph_size")

    adj = complete(m_0)
    for _ in range(m_0, graph_size):
        current_size = len(adj[0, :])
        edge_prob = np.count_nonzero(adj, axis=0).astype(float)
        edge_prob = edge_prob / np.sum(edge_prob)

        adj = np.append(adj, np.zeros((current_size, 1)), axis=1)
        adj = np.append(adj, np.zeros((1, current_size + 1)), axis=0)

        while np.count_nonzero(adj[:, current_size]) == 0:
            for k, probability in enumerate(edge_prob):
                roll = np.random.binomial(1, probability)
                if roll != 0:
                    adj[k, current_size] = roll
                    adj[current_size, k] = roll

    return adj


def erdos(g_size, subtype):
    """
    Convenience selector for canned stochastic-block graph presets.
    """

    g_size = _require_int("g_size", g_size, minimum=1)

    if subtype == "o":
        return erdos_orig(g_size)
    if subtype == "a":
        return erdos_a(g_size)
    if subtype == "d":
        return erdos_d(g_size)
    raise ValueError("subtype must be one of 'o', 'a', or 'd'")


def erdos_orig(g_size):
    """
    Return a one-community stochastic block graph.
    """

    prob = 0.01
    adj, _ = erdos_planted(g_size, 1, prob)
    return adj


def erdos_a(g_size):
    """
    Return a canned assortative stochastic block graph.
    """

    p_in, p_out, n_comm = 0.1, 0.0001, 6
    adj, _ = erdos_planted(g_size, n_comm, p_in, p_out)
    return adj


def erdos_d(g_size):
    """
    Return a canned disassortative stochastic block graph.
    """

    p_in, p_out, n_comm = 0.0001, 0.1, 6
    adj, _ = erdos_planted(g_size, n_comm, p_in, p_out)
    return adj


def erdos_planted(g_size, n_comm, p_in, p_out=None):
    """
    Retry until a connected stochastic block graph is found.
    """

    params = (g_size, n_comm, p_in, p_out)

    for _ in range(100):
        adj, communities = erdos_nnconn(*params)
        if is_connected(adj):
            return adj, communities

    raise RuntimeError("failed to generate a connected stochastic block graph")


def erdos_nnconn(g_size, n_comm, p_in, p_out=None):
    """
    Return a stochastic block graph without enforcing connectivity.
    """

    g_size = _require_int("g_size", g_size, minimum=1)
    n_comm = _require_int("n_comm", n_comm, minimum=1)
    if n_comm > g_size:
        raise ValueError("n_comm cannot exceed g_size")

    p_in = _require_probability("p_in", p_in)
    if p_out is None:
        p_out = p_in
    else:
        p_out = _require_probability("p_out", p_out)

    communities = np.array_split(np.arange(g_size), n_comm)
    community_sizes = [len(community) for community in communities]

    adj = _sample_symmetric_block(community_sizes[0], p_in)
    existing_size = community_sizes[0]

    for j in range(1, n_comm):
        community_block = _sample_symmetric_block(community_sizes[j], p_in)
        cross_edges = np.random.binomial(
            1,
            p_out,
            existing_size * community_sizes[j],
        ).reshape(existing_size, community_sizes[j])
        adj = np.block(
            [
                [adj, cross_edges],
                [cross_edges.T, community_block],
            ]
        )
        existing_size += community_sizes[j]

    return adj, communities
