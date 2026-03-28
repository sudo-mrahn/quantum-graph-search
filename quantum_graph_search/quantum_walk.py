"""Canonical quantum-walk import surface for ``quantum_graph_search``.

The current implementations still live in the legacy ``qw`` package while the
namespace transition remains in progress. New code should prefer the explicit
series helpers over the older selector-style ``get_ldists()`` wrapper.
"""

from qw import (
    expected_dist,
    get_mean_distance_series,
    get_mean_square_distance_series,
    get_ldists,
    mean_square_dist,
    qwalk,
)
from qw import lintrans, notunitary, unitary
from qw.lintrans import get_lt

__all__ = [
    "expected_dist",
    "get_mean_distance_series",
    "get_mean_square_distance_series",
    "get_ldists",
    "get_lt",
    "lintrans",
    "mean_square_dist",
    "notunitary",
    "qwalk",
    "unitary",
]
