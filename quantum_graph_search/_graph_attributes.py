"""Utilities for computing structural attributes of dense graph matrices."""

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from numpy import linalg as la
from scipy.sparse.csgraph import shortest_path

from quantum_graph_search._validation import require_square_array


def _as_square_array(matrix, *, name="matrix"):
    """
    Coerce matrix to a NumPy array and ensure it is square.
    """

    return require_square_array(matrix, name=name)


def check_symmetric(matrix):
    """
    Return whether a matrix is approximately symmetric.
    """

    matrix = _as_square_array(matrix)
    return np.all(np.abs(matrix - matrix.T) < 1e-8)


def find_distances(adj_mat):
    """
    Return the all-pairs shortest-path distance matrix.
    """

    adj_mat = _as_square_array(adj_mat, name="adj_mat")
    return shortest_path(adj_mat, directed=False, unweighted=True)


def degrees_of(adj_mat):
    """
    Return the degree of each vertex.
    """

    adj_mat = _as_square_array(adj_mat, name="adj_mat")
    return np.count_nonzero(adj_mat, axis=0).astype(float)


def get_eigs_sym(adj_mat):
    """
    Return eigenvalues of a symmetric matrix in ascending order.
    """

    return la.eigvalsh(adj_mat)


def get_eigvals(mat):
    """
    Return eigenvalues of a matrix.
    """

    return la.eigvals(mat)


def get_gap(mat):
    """
    Return the spectral gap of the given matrix.
    """

    eigs = np.sort(get_eigvals(mat))
    return eigs[-1] - max(np.abs(eigs[:-1]))


def is_connected(adj):
    """
    Check whether an undirected graph is connected.
    """

    adj = _as_square_array(adj, name="adj")
    graph = nx.Graph(adj)
    return nx.is_connected(graph)


def plot_eigs(spect, threshold):
    """
    Plot and return a figure of the given eigenvalues.
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
    axes[1].set_xlabel(
        "eigenvalues not within " + str(threshold) + " of 0",
        fontsize=12,
    )
    axes[1].set_xticks([])
    axes[1].set_yticks([])
    axes[1].legend()
    plt.show()

    return fig, axes
