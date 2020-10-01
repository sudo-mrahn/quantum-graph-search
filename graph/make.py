"""
module to generate adjacency matrices of graphs.

created by Alex Ahn
alex.song.ahn@gmail.com
Temple University
Department of Mathematics
"""

import numpy as np
import numpy.random as rd
from scipy.linalg import block_diag
from graph.attributes import is_connected


def complete(g_size):
    """
    complete graph of given size.
    returns the adjacency matrix.

    Note: this method is faster than:
        adj = np.ones((g_size, g_size)) - np.eye(g_size)
    for graphs of sizes < 1e4
    """
    adj = np.ones((g_size, g_size))
    np.fill_diagonal(adj, 0)
    return adj


def tree(g_size):
    """
    randomly generate a graph (tree) with g_size nodes and g_size-1 edges
    """
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

    # make the cycle graph
    adj = np.roll(np.eye(graph_size - num_spikes), -1) + np.roll(
        np.eye(graph_size - num_spikes), 1)
    np.fill_diagonal(adj, 0)
    adj[-1, 0], adj[0, -1] = 1, 1

    # add spikes
    adj = block_diag(adj, np.zeros((num_spikes, num_spikes)))
    spike_at = np.random.randint(0, graph_size - num_spikes, num_spikes)
    for k in range(num_spikes):
        adj[-k - 1, spike_at[k]], adj[spike_at[k], -k - 1] = 1, 1

    return adj


def barabasi(graph_size, m_0):
    """
    Barabasi-Albert model
    generates graph G of size n from a complete graph of size m_0
    returns adjacency matrix
    """
    graph = np.ones((m_0, m_0)) - np.eye(m_0)
    for _ in range(m_0, graph_size):
        current_size = len(graph[0, :])
        edge_prob = np.zeros(current_size)
        for j in range(current_size):
            edge_prob[j] = np.count_nonzero(
                graph[:, j])  # outdegree = number of nonzero in column
            # IMPORTANT: for a vector that goes from node u to node v, u is the
            # column and v is the row.

        edge_prob = edge_prob / np.sum(
            edge_prob
        )  # vector containing the p_i, prob of new node to connect to node i

        # make the adjacency matrix one node bigger
        graph = np.append(graph, np.zeros((current_size, 1)), axis=1)
        graph = np.append(graph, np.zeros((1, current_size + 1)), axis=0)

        # roll to get new edges (roll until success)
        while np.count_nonzero(graph[:, current_size]) == 0:
            for k in range(current_size):
                roll = rd.binomial(
                    1,
                    edge_prob[k])  # 1 is the sample size n of the population
                # i.e. this is just a Bernoulli trial with success probability
                # edge_prob[k]
                # returns the number of successes out of sample size n=1,
                # performed 1 time (default param)
                if roll != 0:  # make sure to add both directions
                    graph[k, current_size] = roll
                    graph[current_size, k] = roll

    return graph


def erdos(g_size, subtype):
    """
    convenience function to defin the properties of the erdos-renyi graph to be
    used in deg_distr
    """

    if subtype == "o":
        adj = erdos_orig(g_size)
    elif subtype == "a":
        adj = erdos_a(g_size)
    elif subtype == "d":
        adj = erdos_d(g_size)
    return adj


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
    same as erdos_nnconn defined below, except that it either returns a
    connected graph or an assertion error.
    """
    params = (g_size, n_comm, p_in, p_out)

    adj, communities = erdos_nnconn(*params)
    count = 0
    while not is_connected(adj):
        adj, communities = erdos_nnconn(*params)
        count += 1
        assert count < 100  # don't try for a connected graph >100 times
    return adj, communities


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

    if p_out is None:
        p_out = p_in

    # partition the graph into communities
    communities = np.array_split(np.arange(g_size), n_comm)

    # list of community sizes
    c_sizes = [len(communities[i]) for i in range(n_comm)]

    adj = np.zeros((c_sizes[0], c_sizes[0]))
    triu_ind = np.triu_indices(c_sizes[0], k=1)
    adj[triu_ind] = list(
        np.random.binomial(1, p_in, int((c_sizes[0] * (c_sizes[0] - 1)) / 2)))
    so_far = c_sizes[0]

    for j in range(1, n_comm):
        pawnee = np.zeros((c_sizes[j], c_sizes[j]))
        triu_ind = np.triu_indices(c_sizes[j], k=1)
        pawnee[triu_ind] = list(
            np.random.binomial(1, p_in, int(
                (c_sizes[j] * (c_sizes[j] - 1)) / 2)))

        eagleton = np.random.binomial(1, p_out,
                                      int(so_far * c_sizes[j])).reshape(
                                          so_far, c_sizes[j])

        adj = np.block([[adj, eagleton],
                        [np.zeros((c_sizes[j], so_far)), pawnee]])

        so_far += c_sizes[j]

    tril = np.tril_indices(g_size, k=-1)
    adj[tril] = adj.T[tril]

    return adj, communities
