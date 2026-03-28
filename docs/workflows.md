# Workflows

This repository is easiest to understand as a small set of workflows built on
top of dense adjacency matrices.

## 1. Graph -> Quantum Search

Typical path:

1. Generate or load an adjacency matrix with `graph.make`.
2. Choose a marked node.
3. Run `qs.unitary.simulate`.
4. Inspect the probability at the marked node over time.

Minimal example:

```python
from graph.make import complete
from qs.unitary import simulate

adj = complete(6)
probabilities = simulate(adj, marked=0, t_1=1, stop=10)
```

## 2. Graph -> Quantum Walk Localization

Typical path:

1. Generate or load an adjacency matrix with `graph.make`.
2. Choose a marked node.
3. Run `qw.unitary.get_ldists`.
4. Inspect the mean distance or mean square distance from the marked node.

Minimal example:

```python
from graph.make import complete
from qw.unitary import get_ldists

adj = complete(6)
mean_distance = get_ldists(adj, marked=0, l_type="md", stop=10)
```

## 3. Graph Variants for Experiments

The functions in `graph.process` support perturbing or modifying graphs for
research experiments. They are useful, but are better viewed as experiment
helpers than as a polished stable API.

## 4. Non-unitary Variants

The `qs.notunitary` and `qw.notunitary` modules are retained because they were
part of the original research workflow. Public readers should start with the
unitary modules first and only use the non-unitary variants when they need that
specific comparison.
