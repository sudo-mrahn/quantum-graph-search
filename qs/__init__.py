"""Compatibility wrappers for quantum search routines and supporting utilities."""

from quantum_graph_search.quantum_search import (
    initialize,
    initialize_loop_state,
    initialize_neighborhood_state,
    initialize_uniform_state,
    modulus,
    search_times,
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
