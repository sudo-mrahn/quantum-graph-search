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
- `quantum_graph_search.quantum_search` for the canonical unitary quantum
  search workflow and state-initialization helpers
- `quantum_graph_search.quantum_walk` for the canonical unitary quantum
  walk/localization workflow and `get_lt()`
- `quantum_graph_search.classical_walk` for simple classical walk utilities

Historical implementations that are kept for reference live under
`archive/legacy/`.

Exploratory notebook material lives under `notebooks/` and is not part of the
supported API.

The older top-level Python packages `graph`, `qs`, `qw`, and `cw` are still
shipped as compatibility layers. The canonical implementations now live under
`quantum_graph_search`, but the legacy imports remain available for older
scripts and notebooks.

## Core Concepts

- Graphs are represented as dense NumPy adjacency matrices.
- Quantum-search and quantum-walk `state` objects are also represented as
  dense matrices whose entries store amplitudes on directed edges.
- Several graph-processing helpers assume that vertex `0` is the marked vertex
  unless a function explicitly accepts a different marked-node argument.
- Research-oriented non-unitary variants are still available through the
  legacy `qs` and `qw` packages.

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

For the standard local development workflow:

```bash
make bootstrap
source .venv/bin/activate
```

If `make bootstrap` cannot create `.venv` with `python3 -m venv` on
Debian/Ubuntu, install the matching `python3-venv` package for your
interpreter and rerun the command. The target also falls back to
`python3 -m virtualenv` when that tool is already available.

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
  Canonical namespaced public API and implementation home for the package.
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
- `archive/legacy/` is historical code. It is not treated as the canonical
  implementation surface.
- Some utilities are research-grade and intentionally compact. The repository
  favors readability and reproducibility over a fully productized API.
- New code should prefer `quantum_graph_search.*`; the shorter legacy package
  names are retained for backward compatibility only.
- Research-only helpers such as `graph.process`, `qs.notunitary`, and
  `qw.notunitary` remain importable through the legacy compatibility modules,
  but they are not part of the supported canonical surface.

## Development

The canonical local validation path is:

```bash
make bootstrap
make test
make lint
```

`make bootstrap` installs the package in editable mode with test dependencies
into `.venv`. The lint command mirrors CI's `flake8` checks. See
[`docs/development.md`](docs/development.md) for the full local workflow.

## Tested Environment

The current publication-prep pass was verified locally with:

- Python 3.13.7
- NumPy 2.4.3
- SciPy 1.17.1
- NetworkX 3.6.1
- Matplotlib 3.10.8

## License

This repository is distributed under the MIT License. See [`LICENSE`](LICENSE).
