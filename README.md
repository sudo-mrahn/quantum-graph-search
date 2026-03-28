# quantum-graph-search

`quantum-graph-search` is a research companion repository for code
used to study
graph generation, classical walks, Grover walks, and flip-flop Grover search on
graphs.

This repository is intended as a cleaned public snapshot of research code on
quantum search and random-graph experiments. It is not presented as a polished
general-purpose graph library.

## Scope

The canonical public code surface is now namespaced under
`quantum_graph_search`:

- `quantum_graph_search.graph` for graph construction and graph attributes
- `quantum_graph_search.quantum_search` for unitary and non-unitary quantum
  search routines
- `quantum_graph_search.quantum_walk` for unitary and non-unitary quantum
  walk/localization routines
- `quantum_graph_search.classical_walk` for simple classical walk utilities

Historical implementations that are kept for reference live under
`archive/legacy/`.

Exploratory notebook material lives under `notebooks/` and is not part of the
supported API.

The older top-level Python packages `graph`, `qs`, `qw`, and `cw` are still
shipped as compatibility layers during the namespace transition, but new code
should prefer `quantum_graph_search.*`.

## Core Concepts

- Graphs are represented as dense NumPy adjacency matrices.
- Quantum-search and quantum-walk `state` objects are also represented as
  dense matrices whose entries store amplitudes on directed edges.
- Several graph-processing helpers assume that vertex `0` is the marked vertex
  unless a function explicitly accepts a different marked-node argument.
- `unitary` and `notunitary` modules are both retained because both were part
  of the original research workflow.

## Installation

This project targets Python 3.8+.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

For test dependencies:

```bash
pip install -e .[test]
```

Alternatively:

```bash
pip install -r requirements.txt
```

## Quick Start

```python
import numpy as np

from quantum_graph_search.graph import complete
from quantum_graph_search.quantum_search import simulate as simulate_qs
from quantum_graph_search.quantum_walk import get_mean_distance_series

np.random.seed(0)

adj = complete(6)
marked = 0

qs_probabilities = simulate_qs(adj, marked=marked, t_1=1, stop=5)
qw_mean_distance = get_mean_distance_series(adj, marked=marked, stop=5)

print(qs_probabilities)
print(qw_mean_distance)
```

See [`examples/basic_usage.py`](examples/basic_usage.py) for a runnable
example.

See [`docs/migration.md`](docs/migration.md) for the old-to-new import map.
For new quantum-walk code, prefer
`get_mean_distance_series()` / `get_mean_square_distance_series()` over the
older selector-style `get_ldists()` wrapper.

## Repository Layout

- [`quantum_graph_search/`](quantum_graph_search)
  Canonical namespaced public API for the package.
- [`graph/`](graph)
  Legacy compatibility package for graph generation and graph-processing
  helpers.
- [`qs/`](qs)
  Legacy compatibility package for quantum search operators and supporting
  utilities.
- [`qw/`](qw)
  Legacy compatibility package for quantum walk localization and
  linear-transformation helpers.
- [`cw/`](cw)
  Legacy compatibility package for classical random walk utilities and a small
  CLI-oriented script.
- [`archive/legacy/`](archive/legacy)
  Historical implementations retained for reference.
- [`notebooks/`](notebooks)
  Exploratory notebooks retained as supplemental material.
- [`tests/`](tests)
  Minimal smoke tests for packaging and core functionality.

## Project Notes

- Most routines operate on dense NumPy adjacency matrices.
- Several graph-transformation routines assume that vertex `0` is the marked
  vertex unless otherwise stated.
- `unitary` and `notunitary` modules are both included because both were part
  of the research workflow.
- `archive/legacy/` is historical code. It is not treated as the canonical
  implementation surface.
- Some utilities are research-grade and intentionally compact. The repository
  favors readability and reproducibility over a fully productized API.
- New code should prefer `quantum_graph_search.*`; the shorter legacy package
  names are retained for backward compatibility only.

## Development

Run tests from the repository root:

```bash
python3 -m pytest
```

## Tested Environment

The current publication-prep pass was verified locally with:

- Python 3.13.7
- NumPy 2.4.3
- SciPy 1.17.1
- NetworkX 3.6.1
- Matplotlib 3.10.8

## License

This repository is distributed under the MIT License. See [`LICENSE`](LICENSE).
