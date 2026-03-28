# API Map

This document identifies the intended public entry points for the current
public release of `quantum-graph-search`.

## Canonical Public Modules

- `quantum_graph_search.graph`
- `quantum_graph_search.quantum_search`
- `quantum_graph_search.quantum_walk`
- `quantum_graph_search.classical_walk`

## Recommended Public Entry Points

### quantum_graph_search.graph

Primary constructors and helpers:

- `quantum_graph_search.graph.complete`
- `quantum_graph_search.graph.tree`
- `quantum_graph_search.graph.cycle`
- `quantum_graph_search.graph.barabasi`
- `quantum_graph_search.graph.erdos`
- `quantum_graph_search.graph.erdos_planted`
- `quantum_graph_search.graph.erdos_nnconn`
- `quantum_graph_search.graph.degrees_of`
- `quantum_graph_search.graph.find_distances`
- `quantum_graph_search.graph.is_connected`

These are the clearest public functions for graph generation and graph
structure.

### quantum_graph_search.quantum_search

Primary public entry points:

- `quantum_graph_search.quantum_search.initialize`
- `quantum_graph_search.quantum_search.initialize_loop_state`
- `quantum_graph_search.quantum_search.initialize_neighborhood_state`
- `quantum_graph_search.quantum_search.initialize_uniform_state`
- `quantum_graph_search.quantum_search.modulus`
- `quantum_graph_search.quantum_search.search_times`
- `quantum_graph_search.quantum_search.oracle`
- `quantum_graph_search.quantum_search.coin`
- `quantum_graph_search.quantum_search.shift`
- `quantum_graph_search.quantum_search.qsearch`
- `quantum_graph_search.quantum_search.prob`
- `quantum_graph_search.quantum_search.simulate`

These are the canonical entry points for the unitary quantum-search workflow.

### quantum_graph_search.quantum_walk

Primary public entry points:

- `quantum_graph_search.quantum_walk.qwalk`
- `quantum_graph_search.quantum_walk.expected_dist`
- `quantum_graph_search.quantum_walk.mean_square_dist`
- `quantum_graph_search.quantum_walk.get_mean_distance_series`
- `quantum_graph_search.quantum_walk.get_mean_square_distance_series`
- `quantum_graph_search.quantum_walk.get_lt`

These are the canonical entry points for the unitary quantum-walk workflow.
The older selector-style `quantum_graph_search.quantum_walk.get_ldists` helper
is retained for compatibility, but new code is clearer when it calls one of
the explicit series functions above.

### quantum_graph_search.classical_walk

Primary public entry points:

- `quantum_graph_search.classical_walk.step`
- `quantum_graph_search.classical_walk.walk`
- `quantum_graph_search.classical_walk.return_times`
- `quantum_graph_search.classical_walk.run_cycle_demo`

## Legacy Compatibility Modules

- `graph`
- `qs`
- `qw`
- `cw`

These remain importable for backward compatibility, but they are no longer the
recommended public import surface.

## Research-Only or Internal Helpers

- `graph.process`
  Useful for experiment setup, but not a polished stable API.
- `qs.notunitary`
  Kept because it was part of the research workflow.
- `qw.notunitary`
  Kept because it was part of the research workflow.
- Older sampling helpers in `qs.unitary` and `qw.unitary`
  Retained for research continuity, but not the clearest public API.
- `archive/legacy/*`
  Historical implementations only.
