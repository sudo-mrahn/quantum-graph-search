"""Unitary Grover walk and localization utilities."""

import numpy as np
import warnings

from qw._localization import (
    resolve_localization_series,
    run_localization_series,
    sample_localization_series,
)
from qs.process import initialize_neighborhood_state
from qs.unitary import coin, prob, shift


def expected_dist(state, node, distances, adj):
    """
    **corrected version**

    mean distance of state wrt given node
    returns a real number
    """
    r_t = 0
    for vertex in range(len(state[:, 0])):
        r_t += distances[vertex, node] * prob(state, vertex, adj)
    return r_t


def mean_square_dist(state, marked, distances, adj):
    """
    **corrected version**

    mean square distance of state from given node
    returns a real number
    """
    square_dist = np.square(distances)
    msd = 0
    for node in range(len(state)):
        msd += square_dist[node, marked] * prob(state, node, adj)
    return msd


def qwalk(state, deg, adj):
    """
    **corrected version**

    run 1 step of qw

    returns a 2-d array containing the quantum state after shift and coin
    """
    return shift(coin(state, deg, adj), adj)


def get_mean_distance_series(adj, marked, stop):
    """
    return the mean distance from marked over time.
    """
    return run_localization_series(
        adj,
        marked,
        stop,
        initialize_state_fn=initialize_neighborhood_state,
        walk_step_fn=qwalk,
        measure_fn=lambda state, node, distances, graph: expected_dist(
            state, node, distances, graph
        ),
    )


def get_mean_square_distance_series(adj, marked, stop):
    """
    return the mean square distance from marked over time.
    """
    return run_localization_series(
        adj,
        marked,
        stop,
        initialize_state_fn=initialize_neighborhood_state,
        walk_step_fn=qwalk,
        measure_fn=lambda state, node, distances, graph: mean_square_dist(
            state, node, distances, graph
        ),
    )


def get_ldists(adj, marked, l_type, stop):
    """
    simulate a quantum walk for timesteps up to 'stop' while measuring the
    localization of the quantum state wrt. the marked vertex at each step.

    returns a list of localization measures (mean distance or mean square
    distance) over all timesteps.

    note that this function usees the unitary quantum operators.
    """

    series_fn = resolve_localization_series(
        l_type, get_mean_distance_series, get_mean_square_distance_series
    )
    return series_fn(adj, marked, stop)


# -----------------------------------------------------------------------------
# This is pretty old code. let's rewrite what we can above.
# In fact everything below should be deprecated and replaced with new code.

def _sample_localization(
    adj_mat, marked_node_indices, initial, maxss, total_steps, measure
):
    return sample_localization_series(
        adj_mat,
        marked_node_indices,
        initial,
        maxss,
        total_steps,
        walk_step_fn=qwalk,
        measure_fn=measure,
    )


def sample_r(adj_mat, marked_node_indices, initial, maxss, total_steps):
    """
    **corrected version**

    run qw on given sample of nodes
    given adjacency matrix adj_mat, 1-d array of indices marked_node_indices
    returns r_t
    """

    warnings.warn(
        "sample_r() is a legacy helper; prefer get_mean_distance_series().",
        DeprecationWarning,
        stacklevel=2,
    )
    return _sample_localization(
        adj_mat, marked_node_indices, initial, maxss, total_steps, expected_dist
    )


def sample_v(adj_mat, marked_node_indices, initial, maxss, total_steps):
    """
    **corrected version**

    run qw on given sample of nodes
    given adjacency matrix adj_mat, 1-d array of indices marked_node_indices
    returns v_t
    """

    warnings.warn(
        "sample_v() is a legacy helper; prefer get_mean_square_distance_series().",
        DeprecationWarning,
        stacklevel=2,
    )
    return _sample_localization(
        adj_mat, marked_node_indices, initial, maxss, total_steps, mean_square_dist
    )
