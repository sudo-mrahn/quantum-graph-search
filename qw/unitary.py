"""Unitary Grover walk and localization utilities."""

import warnings
import numpy as np

from qw._legacy_sampling import sample_localization_measure_series
from qw._localization import (
    resolve_localization_series,
    run_localization_series,
)
from qs.process import initialize_neighborhood_state
from qs.unitary import coin, prob, shift


def expected_dist(state, node, distances, adj):
    """
    Return the mean graph distance from ``node`` under the current state.
    """
    r_t = 0
    for vertex in range(len(state[:, 0])):
        r_t += distances[vertex, node] * prob(state, vertex, adj)
    return r_t


def mean_square_dist(state, marked, distances, adj):
    """
    Return the mean square graph distance from ``marked``.
    """
    square_dist = np.square(distances)
    msd = 0
    for node in range(len(state)):
        msd += square_dist[node, marked] * prob(state, node, adj)
    return msd


def qwalk(state, deg, adj):
    """
    Run one unitary quantum-walk step and return the next state.
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
        measure_fn=expected_dist,
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
        measure_fn=mean_square_dist,
    )


def get_ldists(adj, marked, l_type, stop):
    """
    Compatibility wrapper over the explicit localization-series helpers.

    New code should prefer ``get_mean_distance_series()`` or
    ``get_mean_square_distance_series()`` directly.
    """

    series_fn = resolve_localization_series(
        l_type, get_mean_distance_series, get_mean_square_distance_series
    )
    return series_fn(adj, marked, stop)


def _sample_localization(
    adj_mat, marked_node_indices, initial, maxss, total_steps, measure
):
    """
    Run the historical multi-marked-node localization workflow.
    """

    return sample_localization_measure_series(
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
    Deprecated compatibility wrapper for mean-distance sampling.
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
    Deprecated compatibility wrapper for mean-square-distance sampling.
    """

    warnings.warn(
        "sample_v() is a legacy helper; prefer get_mean_square_distance_series().",
        DeprecationWarning,
        stacklevel=2,
    )
    return _sample_localization(
        adj_mat, marked_node_indices, initial, maxss, total_steps, mean_square_dist
    )
