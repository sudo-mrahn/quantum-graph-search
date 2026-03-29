"""Canonical quantum-search import surface for ``quantum_graph_search``.

Research-oriented non-unitary and helper modules remain available through the
legacy ``qs`` compatibility package.
"""

from quantum_graph_search._quantum_search_process import (
    initialize,
    initialize_loop_state,
    initialize_neighborhood_state,
    initialize_uniform_state,
    modulus,
    search_times,
)
from quantum_graph_search._quantum_search_unitary import (
    coin,
    oracle,
    prob,
    qsearch,
    shift,
    simulate,
)
__all__ = [
    "coin",
    "initialize",
    "initialize_loop_state",
    "initialize_neighborhood_state",
    "initialize_uniform_state",
    "modulus",
    "oracle",
    "prob",
    "qsearch",
    "search_times",
    "shift",
    "simulate",
]
