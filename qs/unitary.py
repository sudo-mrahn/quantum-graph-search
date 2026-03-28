"""Unitary flip-flop Grover search on dense graph adjacency matrices."""

import numpy as np
import warnings

from qs._simulation import run_probability_series, sample_probability_series


# corrected operators
# i.e. these are unitary.
def oracle(state, marked_node, adj):
    """
    unitary oracle operator
    """
    new_state = np.array(state, dtype=float, copy=True)
    new_state[:, marked_node] -= (
        2 * adj[:, marked_node] * new_state[:, marked_node]
    )
    return new_state


def coin(state, deg, adj):
    """
    unitary version of the coin operator

    i.e. the Hilbert space acted on by this function is NOT the augmented
    Hilbert space of the directed edges of the completion of the graph
    represented by the adjacency matrix input.

    rather, it is the proper Hilbert space of directed edges represented in adj
    """

    new_state = np.array(state, dtype=float, copy=True)
    for i in range(len(adj)):
        # sum coefficients of vectors
        ampl_sum = np.dot(adj[:, i], state[:, i])
        if deg[i] == 0:
            raise ValueError("coin operator is undefined on isolated vertices")
        new_state[:, i] -= (2 * ampl_sum / deg[i]) * adj[:, i]

    return -1 * new_state


def shift(state, adj):
    """
    unitary shift operator
    """
    return (state * adj).T


def qsearch(state, deg, adj, marked_node, t_1):
    """
    one iteration of the quantum search
    returns a new quantum state after applying the qs operator

    state: input quantum state in the form of a 2-d array
    deg: 1-d array of degrees of the vertex identified with the array index
    adj: adjacency matrix of the graph
    marked_node: index of marked vertex
    t_1: number of times to apply quantum walk operator after each oracle query
    """

    new_state = oracle(state, marked_node, adj)
    for _ in range(t_1):
        new_state = shift(coin(new_state, deg, adj), adj)

    return new_state


def simulate(adj, marked, t_1, stop):
    """
    many iterations of the quantum search.
    returns an array (list) of probabilities at the marked vertex.

    stop: total number of qs iterations
    """

    return run_probability_series(
        adj,
        marked,
        stop,
        step_fn=lambda state, degrees, graph, marked_node: qsearch(
            state, degrees, graph, marked_node, t_1
        ),
        probability_fn=lambda state, marked_node, graph: prob(
            state, marked_node, graph
        ),
    )


def prob(state, marked, adj):
    """
    corrected probability at given vertex
    """
    return np.sum((state[:, marked] * adj[:, marked])**2)


def _sample_probabilities(adj_mat, node_indices, maxss, total_steps, t_1):
    """
    legacy helper that samples probabilities for multiple marked nodes.
    """
    return sample_probability_series(
        adj_mat,
        node_indices,
        maxss,
        total_steps,
        step_fn=lambda state, degrees, graph, marked_node: qsearch(
            state, degrees, graph, marked_node, t_1
        ),
        probability_fn=lambda state, marked_node, graph: prob(
            state, marked_node, graph
        ),
    )


def sample(adj_mat, node_indices, maxss, total_steps, t_1):
    """
    deprecated compatibility wrapper for the legacy sampling helper.
    """

    warnings.warn(
        "sample() is a legacy helper; prefer simulate() for the public API.",
        DeprecationWarning,
        stacklevel=2,
    )
    return _sample_probabilities(adj_mat, node_indices, maxss, total_steps, t_1)
