"""Compatibility wrappers for graph structural helpers."""

from quantum_graph_search._graph_attributes import (
    check_symmetric,
    degrees_of,
    find_distances,
    get_eigs_sym,
    get_eigvals,
    get_gap,
    is_connected,
    plot_eigs,
)

__all__ = [
    "check_symmetric",
    "degrees_of",
    "find_distances",
    "get_eigs_sym",
    "get_eigvals",
    "get_gap",
    "is_connected",
    "plot_eigs",
]
