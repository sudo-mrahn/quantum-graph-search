"""Internal helpers for quantum-search probability time series."""

import numpy as np

from graph.attributes import degrees_of
from qs.process import initialize_uniform_state


def run_probability_series(adj, marked, stop, *, step_fn, probability_fn):
    """
    run a marked-vertex probability time series for a single graph.
    """

    degrees = degrees_of(adj)
    state = initialize_uniform_state(adj)
    probabilities = []

    for _ in range(stop + 1):
        probabilities.append(probability_fn(state, marked, adj))
        state = step_fn(state, degrees, adj, marked)

    return probabilities


def sample_probability_series(
    adj_mat,
    node_indices,
    maxss,
    total_steps,
    *,
    step_fn,
    probability_fn,
):
    """
    run legacy marked-node sampling for multiple quantum-search simulations.
    """

    nsamples = min(maxss, len(node_indices))
    probabilities = np.zeros((total_steps + 1, nsamples))
    degrees = degrees_of(adj_mat)
    initial_state = initialize_uniform_state(adj_mat)
    progress_interval = max(1, int(np.round(max(nsamples, 1) / 10)))

    for column, marked_node in enumerate(node_indices[:nsamples].astype(int)):
        state = np.array(initial_state, dtype=float, copy=True)
        probabilities[0, column] = probability_fn(state, marked_node, adj_mat)

        for i in range(1, total_steps + 1):
            state = step_fn(state, degrees, adj_mat, marked_node)
            probabilities[i, column] = probability_fn(state, marked_node, adj_mat)

        if (column + 1) % progress_interval == 0:
            print(str(np.round(100 * (column + 1) / nsamples, 1)) + "% complete")

    return probabilities
