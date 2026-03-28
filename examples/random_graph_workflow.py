"""End-to-end example using a random graph with search and walk workflows."""

import numpy as np

from quantum_graph_search.graph import erdos_planted
from quantum_graph_search.quantum_search import simulate as simulate_qs
from quantum_graph_search.quantum_walk import get_ldists


def main():
    np.random.seed(0)

    adj, communities = erdos_planted(12, 3, 0.5, 0.1)
    marked = int(communities[0][0])

    qs_probabilities = simulate_qs(adj, marked=marked, t_1=1, stop=8)
    qw_msd = get_ldists(adj, marked=marked, l_type="msd", stop=8)

    print("Marked node:", marked)
    print("Community sizes:", [len(comm) for comm in communities])
    print("Quantum search probabilities:")
    print(qs_probabilities)
    print()
    print("Quantum walk mean square distance:")
    print(qw_msd)


if __name__ == "__main__":
    main()
