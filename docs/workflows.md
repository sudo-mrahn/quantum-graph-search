# Workflows

This repository is easiest to understand as a small set of workflows built on
top of dense adjacency matrices.

## 1. Graph -> Quantum Search

Typical path:

1. Generate or load an adjacency matrix with `quantum_graph_search.graph`.
2. Choose a marked node.
3. Run `quantum_graph_search.quantum_search.simulate`.
4. Inspect the probability at the marked node over time.

Minimal example:

```python
from quantum_graph_search.graph import complete
from quantum_graph_search.quantum_search import simulate

adj = complete(6)
probabilities = simulate(adj, marked=0, t_1=1, stop=10)
```

## 2. Graph -> Quantum Walk Localization

Typical path:

1. Generate or load an adjacency matrix with `quantum_graph_search.graph`.
2. Choose a marked node.
3. Run `quantum_graph_search.quantum_walk.get_mean_distance_series` or
   `quantum_graph_search.quantum_walk.get_mean_square_distance_series`.
4. Inspect the mean distance or mean square distance from the marked node.

Minimal example:

```python
from quantum_graph_search.graph import complete
from quantum_graph_search.quantum_walk import get_mean_distance_series

adj = complete(6)
mean_distance = get_mean_distance_series(adj, marked=0, stop=10)
```

## 3. Graph Variants for Experiments

The functions in `graph.process` support perturbing or modifying graphs for
research experiments. They remain available through the legacy compatibility
package, but they are better viewed as experiment helpers than as a polished
stable API and are intentionally left outside the canonical public namespace.

## 4. Non-unitary Variants

The `qs.notunitary` and `qw.notunitary` modules are retained because they were
part of the original research workflow. Public readers should start with
`quantum_graph_search.quantum_search` and
`quantum_graph_search.quantum_walk` first and only use the legacy non-unitary
variants when they need that specific comparison.

The selector-style `get_ldists()` helper is still available for compatibility,
but new code is usually clearer when it calls the explicit mean-distance or
mean-square-distance series function directly.
