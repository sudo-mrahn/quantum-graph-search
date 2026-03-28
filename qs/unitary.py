"""Unitary flip-flop Grover search on dense graph adjacency matrices."""

import warnings
import numpy as np

from qs._legacy_sampling import sample_marked_probability_series
from qs._simulation import run_probability_series


def oracle(state, marked_node, adj):
    """
    Apply the marked-vertex oracle for the unitary search model.
    """
    new_state = np.array(state, dtype=float, copy=True)
    new_state[:, marked_node] -= (
        2 * adj[:, marked_node] * new_state[:, marked_node]
    )
    return new_state


def coin(state, deg, adj):
    """
    Apply the Grover coin on the directed-edge Hilbert space.

    This acts on the directed edges present in ``adj``, not on an augmented
    completion of the graph.
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
    Swap edge directions after masking by the graph adjacency.
    """
    return (state * adj).T


def qsearch(state, deg, adj, marked_node, t_1):
    """
    Run one quantum-search iteration and return the next state.

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
    Run the unitary quantum-search time series.

    stop: total number of qs iterations
    """

    return run_probability_series(
        adj,
        marked,
        stop,
        step_fn=lambda state, degrees, graph, marked_node: qsearch(
            state, degrees, graph, marked_node, t_1
        ),
        probability_fn=prob,
    )


def prob(state, marked, adj):
    """
    Return the probability mass at ``marked``.
    """
    return np.sum((state[:, marked] * adj[:, marked]) ** 2)


def _sample_probabilities(adj_mat, node_indices, maxss, total_steps, t_1):
    """
    Run the historical multi-marked-node sampling workflow.
    """
    return sample_marked_probability_series(
        adj_mat,
        node_indices,
        maxss,
        total_steps,
        step_fn=lambda state, degrees, graph, marked_node: qsearch(
            state, degrees, graph, marked_node, t_1
        ),
        probability_fn=prob,
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
