"""
module to retrieve various attributes of a graph

created by Alex Ahn
alex.song.ahn@gmail.com
Temple University
Department of Mathematics
"""

import numpy as np
import matplotlib.pyplot as plt
from numpy import linalg as la
from scipy.sparse.csgraph import shortest_path


def check_symmetric(matrix):
    """
    just a quick function to check if a given matrix is approximately symmetric
    """
    return np.all(np.abs(matrix - matrix.T) < 1e-8)


def find_distances(adj_mat):
    """
    quick function to retrieve matrix of distances between vertices
    """
    return shortest_path(adj_mat, directed=False, unweighted=True)


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


def get_eigs_sym(adj_mat):
    """
    returns an array of eigenvalues of a symmetric matrix
    eigenvalues are stored in ascending order
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


def is_connected(adj):
    """
    returns True if adj is the adjacency matrix of a connected graph
    False if not.

    this method uses the property of the Fiedler eigenvalue, namely that it is
    positive if and only if the graph is connected.

    Fiedler eigenvalue is defined to be the second smallest eigenvalue of the
    graph laplacian matrix, L = D - A, where D is the degree matrix and A the
    adjacency matrix of the graph.
    """

    # don't use this for large graphs
    assert len(adj) < 3000

    eigs = get_eigs_sym(np.diag(degrees_of(adj)) - adj)

    return eigs[1] > 0


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
