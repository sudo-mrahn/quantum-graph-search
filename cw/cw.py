"""Compatibility wrappers for classical random walk utilities."""

from quantum_graph_search._classical_walk import main, return_times, run_cycle_demo, step, walk

__all__ = [
    "main",
    "return_times",
    "run_cycle_demo",
    "step",
    "walk",
]


if __name__ == "__main__":
    import sys

    main(sys.argv[1:])
