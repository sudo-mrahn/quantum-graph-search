# Migration Guide

Use the `quantum_graph_search` namespace for new code.

## Old to New Imports

- `from graph import complete`
  becomes `from quantum_graph_search.graph import complete`
- `from graph.make import erdos_planted`
  becomes `from quantum_graph_search.graph import erdos_planted`
- `from qs import simulate`
  becomes `from quantum_graph_search.quantum_search import simulate`
- `from qs.unitary import simulate`
  becomes `from quantum_graph_search.quantum_search import simulate`
- `from qw import get_ldists`
  becomes `from quantum_graph_search.quantum_walk import get_ldists`
- `from qw.lintrans import get_lt`
  becomes `from quantum_graph_search.quantum_walk import get_lt`
- `from cw import walk`
  becomes `from quantum_graph_search.classical_walk import walk`

## Compatibility Policy

The legacy top-level packages `graph`, `qs`, `qw`, and `cw` are still present
so older notebooks and scripts keep working. New public examples, tests, and
documentation now prefer the namespaced package.

For new quantum-walk code, prefer the explicit
`get_mean_distance_series()` / `get_mean_square_distance_series()` APIs over
the older selector-style `get_ldists()` wrapper.
