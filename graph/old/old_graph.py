"""
module to create, manipulate, and study random graphs.

created by Alex Ahn
alex.song.ahn@gmail.com
last edited Aug 31 2020
Temple University
Department of Mathematics
"""

import numpy as np
import numpy.random as rd
import matplotlib.pyplot as plt
from numpy import linalg as la
from scipy.linalg import block_diag
import networkx as nx


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


def degrees_of(adj_mat):
    """
    retrieve degrees of vertices
    given adjacency matrix
    returns vector of degrees of each node
    """
    deg = np.zeros(len(adj_mat))
    for i in range(len(adj_mat)):
        deg[i] = np.count_nonzero(adj_mat[:, i])
        # outdegree = number of nonzero in column
    return deg


def pick_nodes(adj_mat, setting, num):
    """
    pick node samples
    num should be int for setting in ['l', 'h']
    and list for setting == 'm'
    """
    degrees = degrees_of(adj_mat)
    error_message = "invalid input for pick_nodes"
    if setting in ("low", "l"):
        if isinstance(num, int):
            nodes = np.argwhere(degrees <= num)[:, 0]
        else:
            print(error_message)
    elif setting in ("medium", "m"):
        if isinstance(num, list):
            nodes = np.argwhere(np.isin(degrees, num))[:, 0]
        else:
            print(error_message)
    elif setting in ("high", "h"):
        if isinstance(num, int):
            nodes = np.argwhere(degrees >= num)[:, 0]
        else:
            print(error_message)
    else:
        print(error_message)
    return nodes


def get_eigs_sym(adj_mat):
    """
    returns an array of eigenvalues of a symmetric matrix
    """
    return la.eigvalsh(adj_mat)


def get_eigvals(mat):
    """
    returns an array of eigenvalues of a matrix
    """
    return la.eigvals(mat)


def get_gap(mat):
    """
    returns the gap of the given matrix
    """
    eigs = np.sort(get_eigvals(mat))
    return eigs[-1] - max(np.abs(eigs[:-1]))


def plot_eigs(spect, threshold):
    """
    plots and saves a figure showing the given set of eigenvalues
    """
    spect = np.sort(spect)
    gap = spect[-1] - max(np.abs(spect[:-1]))
    spect_nonzero = spect[np.nonzero(np.abs(spect) > threshold)]

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("spectrum of G", fontsize=14)
    axes[0].plot(spect, "o", label="count: " + str(len(spect)))
    axes[0].axhline(spect[-1], color="maroon", lw=0.5, label="gap: %.3e" % gap)
    axes[0].set_xticks([])
    axes[0].set_xlabel("all eigenvalues", fontsize=12)
    axes[0].set_ylabel("eigenvalues", fontsize=12)
    axes[0].legend()

    axes[1].plot(spect_nonzero, "o", label="count: " + str(len(spect_nonzero)))
    axes[1].set_xlabel("eigenvalues not within " + str(threshold) + " of 0",
                       fontsize=12)
    axes[1].set_xticks([])
    axes[1].set_yticks([])
    axes[1].legend()
    plt.show()

    return fig, axes

    # fig.savefig("./figures/plot of spectrum.png", format="png", dpi=600)


# testing main method
def main():
    """
    test main method
    """

    plt.subplots()
    bar_adj = barabasi(5, 2)
    bar_nx = nx.Graph(bar_adj)
    nx.draw(bar_nx)
    plt.show()


if __name__ == "__main__":
    main()
    print("yayyy!!!")
