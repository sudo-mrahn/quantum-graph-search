"""Canonical public namespace for the quantum-graph-search repository.

Public code should import from ``quantum_graph_search.*``.
The canonical implementations now live in this package. The legacy ``graph``,
``qs``, ``qw``, and ``cw`` packages remain importable as compatibility layers.
"""

from . import classical_walk, graph, quantum_search, quantum_walk

__all__ = [
    "classical_walk",
    "graph",
    "quantum_search",
    "quantum_walk",
]
