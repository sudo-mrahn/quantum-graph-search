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
