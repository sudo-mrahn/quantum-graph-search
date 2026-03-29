"""Internal helpers for canonical quantum-walk localization time series."""

import numpy as np

from quantum_graph_search._graph_attributes import degrees_of, find_distances
from quantum_graph_search._quantum_search_process import (
    initialize_loop_state,
    initialize_neighborhood_state,
)
from quantum_graph_search._validation import require_int, require_square_array, require_vertex_index


def resolve_localization_series(l_type, mean_distance_series_fn, mean_square_series_fn):
    """
    Choose the localization series function from a public selector string.
    """

    if l_type in ("md", "mean_distance"):
        return mean_distance_series_fn
    if l_type in ("msd", "mean_square_distance"):
        return mean_square_series_fn
    raise ValueError("l_type must be one of 'md' or 'msd'")


def initialize_sample_state(adj_mat, marked, initial):
    """
    Initialize legacy sampling states from the historical selector string.
    """

    if initial in ["loop", "l"]:
        return initialize_loop_state(adj_mat, marked)
    if initial in ["nbhd", "n"]:
        return initialize_neighborhood_state(adj_mat, marked)
    raise ValueError("initial must be one of 'loop' or 'nbhd'")


def run_localization_series(
    adj,
    marked,
    stop,
    *,
    initialize_state_fn,
    walk_step_fn,
    measure_fn,
):
    """
    Run a localization time series for one marked node.
    """

    adj = require_square_array(adj, name="adj")
    marked = require_vertex_index(adj, marked, name="marked")
    stop = require_int("stop", stop, minimum=0)
    distances = find_distances(adj)
    degrees = degrees_of(adj)
    state = initialize_state_fn(adj, marked)
    localization = []

    for _ in range(stop + 1):
        localization.append(measure_fn(state, marked, distances, adj))
        state = walk_step_fn(state, degrees, adj)

    return localization


def sample_localization_series(
    adj_mat,
    marked_node_indices,
    initial,
    maxss,
    total_steps,
    *,
    walk_step_fn,
    measure_fn,
):
    """
    Run legacy localization sampling for multiple marked nodes.
    """

    adj_mat = require_square_array(adj_mat, name="adj_mat")
    maxss = require_int("maxss", maxss, minimum=0)
    total_steps = require_int("total_steps", total_steps, minimum=0)
    distances = find_distances(adj_mat)
    degrees = degrees_of(adj_mat)
    nsamples = min(maxss, len(marked_node_indices))
    localization = np.zeros((total_steps + 1, nsamples))
    progress_interval = max(1, int(np.round(max(nsamples, 1) / 10)))

    for column, marked in enumerate(marked_node_indices[:nsamples].astype(int)):
        state = initialize_sample_state(adj_mat, marked, initial)
        localization[0, column] = measure_fn(state, marked, distances, adj_mat)

        for i in range(1, total_steps + 1):
            state = walk_step_fn(state, degrees, adj_mat)
            localization[i, column] = measure_fn(state, marked, distances, adj_mat)

        if (column + 1) % progress_interval == 0:
            print(str(np.round(100 * (column + 1) / nsamples, 1)) + "% complete")

    return localization


def sample_localization_measure_series(
    adj_mat,
    marked_node_indices,
    initial,
    maxss,
    total_steps,
    *,
    walk_step_fn,
    measure_fn,
):
    """
    Compatibility wrapper for historical localization sampling helpers.
    """

    return sample_localization_series(
        adj_mat,
        marked_node_indices,
        initial,
        maxss,
        total_steps,
        walk_step_fn=walk_step_fn,
        measure_fn=measure_fn,
    )
