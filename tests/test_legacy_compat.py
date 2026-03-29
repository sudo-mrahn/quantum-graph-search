import numpy as np

from cw import walk as legacy_walk
from graph.process import count_edges, fill_to_total_edges
from qs import simulate as legacy_simulate
from qw import get_mean_distance_series as legacy_mean_distance

from quantum_graph_search.graph import complete, tree
from quantum_graph_search.quantum_search import simulate as canonical_simulate
from quantum_graph_search.quantum_walk import (
    get_mean_distance_series as canonical_mean_distance,
)


def test_legacy_graph_process_wrapper_still_works():
    np.random.seed(0)
    adj = tree(5)

    filled = fill_to_total_edges(adj, total=6)

    assert count_edges(adj) == 4
    assert count_edges(filled) == 6


def test_legacy_quantum_search_wrapper_matches_canonical_output():
    adj = complete(2)

    assert np.allclose(
        legacy_simulate(adj, marked=0, t_1=1, stop=3),
        canonical_simulate(adj, marked=0, t_1=1, stop=3),
    )


def test_legacy_quantum_walk_wrapper_matches_canonical_output():
    adj = complete(2)

    assert np.allclose(
        legacy_mean_distance(adj, marked=0, stop=3),
        canonical_mean_distance(adj, marked=0, stop=3),
    )


def test_legacy_classical_walk_wrapper_still_produces_paths():
    np.random.seed(0)
    adj = complete(2)

    assert legacy_walk(adj, start=0, duration=3) == [0, 1, 0, 1]
