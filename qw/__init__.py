"""Compatibility wrappers for quantum-walk routines and supporting utilities."""

from quantum_graph_search.quantum_walk import (
    expected_dist,
    get_ldists,
    get_mean_distance_series,
    get_mean_square_distance_series,
    mean_square_dist,
    qwalk,
)

__all__ = [
    "expected_dist",
    "get_ldists",
    "get_mean_distance_series",
    "get_mean_square_distance_series",
    "mean_square_dist",
    "qwalk",
]
