"""Compatibility wrappers for non-unitary quantum-search functions."""

from quantum_graph_search._quantum_search_notunitary import (
    coin,
    oracle,
    prob,
    qsearch,
    sample,
    shift,
    simulate,
)

__all__ = [
    "coin",
    "oracle",
    "prob",
    "qsearch",
    "sample",
    "shift",
    "simulate",
]
