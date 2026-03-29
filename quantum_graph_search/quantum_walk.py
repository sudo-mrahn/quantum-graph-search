"""Canonical quantum-walk import surface for ``quantum_graph_search``.

Research-oriented non-unitary and helper modules remain available through the
legacy ``qw`` compatibility package.
"""

from quantum_graph_search._quantum_walk_lintrans import get_lt
from quantum_graph_search._quantum_walk_unitary import (
    expected_dist,
    get_mean_distance_series,
    get_mean_square_distance_series,
    get_ldists,
    mean_square_dist,
    qwalk,
)
__all__ = [
    "expected_dist",
    "get_mean_distance_series",
    "get_mean_square_distance_series",
    "get_ldists",
    "get_lt",
    "mean_square_dist",
    "qwalk",
]
