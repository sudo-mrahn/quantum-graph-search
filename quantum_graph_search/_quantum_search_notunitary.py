"""Non-unitary Grover-search variants used in research experiments."""

import warnings

import numpy as np

from quantum_graph_search._quantum_search_simulation import (
    run_probability_series,
    sample_marked_probability_series,
)
from quantum_graph_search._validation import require_int


def oracle(state, marked_node):
    """
    oracle operator
    """
    mat = state.astype(float)
    mat[:, marked_node] = -1 * mat[:, marked_node]
    return mat


def coin(state, deg, adj):
    """
    NOTE: this operator acts on an augmented Hilbert space of all possible node
    pair vectors, not the limited Hilbert space of directed edges specified by
    adj.

    state: quantum state of the graph, represented as a matrix in the shape of
    an adjacency matrix with coefficients of the vectors in the Hilbert space
    as entries
    deg: vector of node degrees
    adj: adjacency matrix of the graph. this may or may NOT be equivalent to
    the state matrix with nonzero entries replaced by 1.
    """

    new_state = np.zeros_like(state)
    current_size = len(new_state[:, 0])

    for i in range(current_size):
        # sum coefficients of vectors
        ampl_sum = np.sum(state[:, i])
        if deg[i] == 0:
            raise ValueError("coin operator is undefined on isolated vertices")
        new_state[:, i] = (2 * ampl_sum / deg[i]) * adj[:, i]

    new_state = new_state - state

    return new_state


def shift(state):
    """
    shift operator
    """
    return np.transpose(state)


def qsearch(state, deg, adj, marked_node, t_1):
    """
    one iteration of the quantum search
    """
    new_state = oracle(state, marked_node)
    for _ in range(t_1):
        new_state = shift(coin(new_state, deg, adj))

    return new_state


def prob(state, vertex):
    """
    probability at given vertex
    """
    neighborhood = state[:, vertex]
    return np.sum(neighborhood**2)


def simulate(adj, marked, t_1, stop):
    """
    many iterations of the quantum search.
    returns an array (list) of probabilities at the marked vertex.

    stop: total number of qs iterations
    """

    t_1 = require_int("t_1", t_1, minimum=0)
    return run_probability_series(
        adj,
        marked,
        stop,
        step_fn=lambda state, degrees, graph, marked_node: qsearch(
            state, degrees, graph, marked_node, t_1
        ),
        probability_fn=lambda state, marked_node, _graph: prob(state, marked_node),
    )


def _sample_probabilities(adj_mat, node_indices, maxss, total_steps, t_1):
    """
    Run the historical multi-marked-node sampling workflow.
    """
    t_1 = require_int("t_1", t_1, minimum=0)
    return sample_marked_probability_series(
        adj_mat,
        node_indices,
        maxss,
        total_steps,
        step_fn=lambda state, degrees, graph, marked_node: qsearch(
            state, degrees, graph, marked_node, t_1
        ),
        probability_fn=lambda state, marked_node, _graph: prob(state, marked_node),
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
