"""Minimal example for the public quantum-graph-search repository."""

import numpy as np

from quantum_graph_search.graph import complete
from quantum_graph_search.quantum_search import simulate as simulate_qs
from quantum_graph_search.quantum_walk import get_mean_distance_series


def main():
    np.random.seed(0)

    adj = complete(6)
    marked = 0

    qs_probabilities = simulate_qs(adj, marked=marked, t_1=1, stop=5)
    qw_mean_distance = get_mean_distance_series(adj, marked=marked, stop=5)

    print("Quantum search probabilities at the marked node:")
    print(qs_probabilities)
    print()
    print("Quantum walk mean distance from the marked node:")
    print(qw_mean_distance)


if __name__ == "__main__":
    main()
