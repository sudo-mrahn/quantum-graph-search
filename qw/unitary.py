"""Compatibility wrappers for unitary quantum-walk functions."""

from quantum_graph_search._quantum_walk_unitary import (
    expected_dist,
    get_ldists,
    get_mean_distance_series,
    get_mean_square_distance_series,
    mean_square_dist,
    qwalk,
    sample_r,
    sample_v,
)

__all__ = [
    "expected_dist",
    "get_ldists",
    "get_mean_distance_series",
    "get_mean_square_distance_series",
    "mean_square_dist",
    "qwalk",
    "sample_r",
    "sample_v",
]
