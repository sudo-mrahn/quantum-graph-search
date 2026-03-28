"""Graph-construction utilities that return dense adjacency matrices."""

import numpy as np
from scipy.linalg import block_diag

from graph.attributes import is_connected


def _require_int(name, value, minimum=None):
    """
    validate integer-valued constructor arguments.
    """

    if not isinstance(value, (int, np.integer)):
        raise TypeError(f"{name} must be an integer")
    if minimum is not None and value < minimum:
        raise ValueError(f"{name} must be at least {minimum}")
    return int(value)


def _require_probability(name, value):
    """
    validate edge probabilities.
    """

    if not isinstance(value, (int, float, np.integer, np.floating)):
        raise TypeError(f"{name} must be a real number")
    if not 0 <= value <= 1:
        raise ValueError(f"{name} must be between 0 and 1")
    return float(value)


def _sample_symmetric_block(size, probability):
    """
    sample an undirected Erdos-Renyi block of the requested size.
    """

    block = np.zeros((size, size))
    triu_ind = np.triu_indices(size, k=1)
    block[triu_ind] = np.random.binomial(1, probability, len(triu_ind[0]))
    block[(triu_ind[1], triu_ind[0])] = block[triu_ind]
    return block


def complete(g_size):
    """
    complete graph of given size.
    returns the adjacency matrix.

    Note: this method is faster than:
        adj = np.ones((g_size, g_size)) - np.eye(g_size)
    for graphs of sizes < 1e4
    """

    g_size = _require_int("g_size", g_size, minimum=1)
    adj = np.ones((g_size, g_size))
    np.fill_diagonal(adj, 0)
    return adj


def tree(g_size):
    """
    randomly generate a graph (tree) with g_size nodes and g_size-1 edges
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
    produces an undirected cycle graph of given size.
    inputs are both integers.
    returns the adjacency matrix.
    """

    graph_size = _require_int("graph_size", graph_size, minimum=3)
    num_spikes = _require_int("num_spikes", num_spikes, minimum=0)
    cycle_size = graph_size - num_spikes
    if cycle_size < 3:
        raise ValueError("graph_size - num_spikes must be at least 3")

    # make the cycle graph
    adj = np.roll(np.eye(cycle_size), -1) + np.roll(np.eye(cycle_size), 1)
    np.fill_diagonal(adj, 0)
    adj[-1, 0], adj[0, -1] = 1, 1

    # add spikes
    adj = block_diag(adj, np.zeros((num_spikes, num_spikes)))
    if num_spikes == 0:
        return adj

    spike_at = np.random.randint(0, cycle_size, num_spikes)
    for k in range(num_spikes):
        adj[-k - 1, spike_at[k]], adj[spike_at[k], -k - 1] = 1, 1

    return adj


def barabasi(graph_size, m_0):
    """
    Barabasi-Albert model
    generates graph G of size n from a complete graph of size m_0
    returns adjacency matrix
    """

    graph_size = _require_int("graph_size", graph_size, minimum=2)
    m_0 = _require_int("m_0", m_0, minimum=2)
    if m_0 > graph_size:
        raise ValueError("m_0 cannot exceed graph_size")

    graph = complete(m_0)
    for _ in range(m_0, graph_size):
        current_size = len(graph[0, :])
        edge_prob = np.count_nonzero(graph, axis=0).astype(float)
        edge_prob = edge_prob / np.sum(edge_prob)

        # make the adjacency matrix one node bigger
        graph = np.append(graph, np.zeros((current_size, 1)), axis=1)
        graph = np.append(graph, np.zeros((1, current_size + 1)), axis=0)

        # roll to get new edges (roll until success)
        while np.count_nonzero(graph[:, current_size]) == 0:
            for k, probability in enumerate(edge_prob):
                roll = np.random.binomial(1, probability)
                if roll != 0:  # make sure to add both directions
                    graph[k, current_size] = roll
                    graph[current_size, k] = roll

    return graph


def erdos(g_size, subtype):
    """
    convenience function to define the properties of the erdos-renyi graph to
    be used in deg_distr
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
    pre-defined original erdos-renyi graph. equivalent to G(g_size, prob)

    returns the adjacency matrix.
    """

    prob = 0.01
    adj, _ = erdos_planted(g_size, 1, prob)
    return adj


def erdos_a(g_size):
    """
    pre-defined assortative stochastic block graph.

    returns the adjacency matrix.
    """

    p_in, p_out, n_comm = 0.1, 0.0001, 6
    adj, _ = erdos_planted(g_size, n_comm, p_in, p_out)
    return adj


def erdos_d(g_size):
    """
    pre-defined disassortative stochastic block graph.

    returns the adjacency matrix.
    """

    p_in, p_out, n_comm = 0.0001, 0.1, 6
    adj, _ = erdos_planted(g_size, n_comm, p_in, p_out)
    return adj


def erdos_planted(g_size, n_comm, p_in, p_out=None):
    """
    same as erdos_nnconn defined below, except that it retries until a
    connected graph is found or the retry budget is exhausted.
    """

    params = (g_size, n_comm, p_in, p_out)

    for _ in range(100):
        adj, communities = erdos_nnconn(*params)
        if is_connected(adj):
            return adj, communities

    raise RuntimeError("failed to generate a connected stochastic block graph")


def erdos_nnconn(g_size, n_comm, p_in, p_out=None):
    """
    Erdos-Renyi model. note that this graph is not necessarily connected!

    The model implemented here is actually the stochastic block model,
    a broader class of random graph model than the ER model,
    in which I have taken the size of each community to be approximately equal.

    parameters
    g_size:     number of vertices in graph
    n_comm:     number of communities, i.e. partitions of graph vertices
    p_in:       prob that two vertices in the same community will have an edge
    p_out:      prob that two vertices in different communities will have an
                edge

    note that if p_in = p_out, we recover the G(n,p) version of the ER model.
    this can be done explicitly, or by leaving out the last arg 'p_out'

    if p_in > p_out, the graph is called assortative
    if p_in < p_out, the graph is called disassortative

    returns adjacency matrix
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

    # partition the graph into communities
    communities = np.array_split(np.arange(g_size), n_comm)

    # list of community sizes
    c_sizes = [len(community) for community in communities]

    adj = _sample_symmetric_block(c_sizes[0], p_in)
    so_far = c_sizes[0]

    for j in range(1, n_comm):
        pawnee = _sample_symmetric_block(c_sizes[j], p_in)
        eagleton = np.random.binomial(1, p_out, so_far * c_sizes[j]).reshape(
            so_far, c_sizes[j]
        )
        adj = np.block([[adj, eagleton], [eagleton.T, pawnee]])
        so_far += c_sizes[j]

    return adj, communities
