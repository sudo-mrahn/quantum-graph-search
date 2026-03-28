import numpy as np
import pytest

from quantum_graph_search.classical_walk import step as classical_step
from quantum_graph_search.graph import complete
from quantum_graph_search.quantum_search import (
    initialize,
    initialize_neighborhood_state,
    simulate as simulate_qs,
)
from quantum_graph_search.quantum_walk import (
    get_ldists,
    get_lt,
    get_mean_distance_series,
)


def test_initialize_nbhd_has_unit_norm():
    adj = complete(4)
    state = initialize_neighborhood_state(adj, marked=0)

    assert state.shape == adj.shape
    assert np.isclose(np.sum(state**2), 1.0)


def test_quantum_search_simulate_returns_expected_length():
    adj = complete(4)
    probabilities = simulate_qs(adj, marked=0, t_1=1, stop=3)

    assert len(probabilities) == 4
    assert all(prob >= 0 for prob in probabilities)


def test_quantum_walk_localization_returns_expected_length():
    adj = complete(4)
    distances = get_ldists(adj, marked=0, l_type="md", stop=3)

    assert len(distances) == 4


def test_descriptive_quantum_walk_wrapper_matches_selector():
    adj = complete(4)

    assert get_mean_distance_series(adj, marked=0, stop=3) == get_ldists(
        adj, marked=0, l_type="mean_distance", stop=3
    )


def test_initialize_invalid_mode_raises_value_error():
    adj = complete(4)

    with pytest.raises(ValueError):
        initialize(adj, mode="bad-mode", marked=0)


def test_get_lt_invalid_operator_raises_value_error():
    adj = complete(4)

    with pytest.raises(ValueError):
        get_lt(adj, operator="shift", method="np.block")


def test_get_lt_rejects_isolated_vertices():
    adj = np.zeros((3, 3))

    with pytest.raises(ValueError):
        get_lt(adj, operator="coin", method="np.block")


def test_classical_step_rejects_isolated_vertices():
    adj = np.zeros((3, 3))

    with pytest.raises(ValueError):
        classical_step(adj, node=0)
