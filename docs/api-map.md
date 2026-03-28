# API Map

This document identifies the intended public entry points for the current
public release of `quantum-graph-search`.

## Canonical Public Modules

- `graph`
- `qs`
- `qw`
- `cw`

## Recommended Public Entry Points

### graph

Primary constructors and helpers:

- `graph.complete`
- `graph.tree`
- `graph.cycle`
- `graph.barabasi`
- `graph.erdos`
- `graph.erdos_planted`
- `graph.erdos_nnconn`
- `graph.degrees_of`
- `graph.find_distances`
- `graph.is_connected`

These are the clearest public functions for graph generation and graph
structure.

### qs

Primary public entry points:

- `qs.initialize`
- `qs.initialize_loop_state`
- `qs.initialize_neighborhood_state`
- `qs.initialize_uniform_state`
- `qs.modulus`
- `qs.search_times`
- `qs.oracle`
- `qs.coin`
- `qs.shift`
- `qs.qsearch`
- `qs.prob`
- `qs.simulate`

These are the canonical entry points for the unitary quantum-search workflow.

### qw

Primary public entry points:

- `qw.qwalk`
- `qw.expected_dist`
- `qw.mean_square_dist`
- `qw.get_ldists`
- `qw.get_mean_distance_series`
- `qw.get_mean_square_distance_series`

These are the canonical entry points for the unitary quantum-walk workflow.

### cw

Primary public entry points:

- `cw.step`
- `cw.walk`
- `cw.return_times`
- `cw.run_cycle_demo`

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
