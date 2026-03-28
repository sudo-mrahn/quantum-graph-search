"""Canonical public namespace for the quantum-graph-search repository.

Public code should import from ``quantum_graph_search.*``.
During the namespace transition, many implementations still live in the
legacy ``graph``, ``qs``, ``qw``, and ``cw`` packages and are re-exported
through this namespace.
"""

from . import classical_walk, graph, quantum_search, quantum_walk

__all__ = [
    "classical_walk",
    "graph",
    "quantum_search",
    "quantum_walk",
]
