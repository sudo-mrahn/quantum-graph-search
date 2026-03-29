"""Classical random walk utilities on dense adjacency matrices."""

import sys

import numpy as np

from quantum_graph_search._graph_make import cycle
from quantum_graph_search._validation import require_int, require_square_array, require_vertex_index


def step(adj, node):
    """
    Return the next step in the random walk from ``node``.
    """

    adj = require_square_array(adj, name="adj")
    node = require_vertex_index(adj, node, name="node")
    neighbors = np.nonzero(adj[:, node])[0]
    if len(neighbors) == 0:
        raise ValueError("cannot take a walk step from an isolated vertex")
    return np.random.choice(neighbors, 1)[0]


def walk(adj, start, duration):
    """
    Run a random walk on a graph for a fixed duration.
    """

    adj = require_square_array(adj, name="adj")
    start = require_vertex_index(adj, start, name="start")
    duration = require_int("duration", duration, minimum=0)
    path = [start]
    for k in range(duration):
        path.append(step(adj, path[k]))

    return path


def return_times(adj, start, n_samples):
    """
    Return times for repeated random walks to return to ``start``.
    """

    adj = require_square_array(adj, name="adj")
    start = require_vertex_index(adj, start, name="start")
    n_samples = require_int("n_samples", n_samples, minimum=0)
    times = []

    for _ in range(n_samples):
        next_node = step(adj, start)
        time = 1
        while next_node != start:
            next_node = step(adj, next_node)
            time += 1
        times.append(time)

    return times


def run_cycle_demo(graph_size, start, duration, num_spikes=6):
    """
    Run and plot a classical walk demo on a spiked cycle graph.
    """

    import matplotlib.pyplot as plt
    import networkx as nx

    temp_adj = cycle(graph_size, num_spikes)
    path = walk(temp_adj, start, duration)
    print(path)
    temp_g = nx.Graph(temp_adj)
    nx.draw(temp_g, with_labels=True)
    print("random walk on a graph of size " + str(graph_size))
    plt.show()
    return path


def main(args):
    """
    CLI entry point for the cycle-graph demo.
    """

    if len(args) != 3:
        raise SystemExit(
            "usage: python -m cw.cw graph_size starting_node total_iterations"
        )

    run_cycle_demo(int(args[0]), int(args[1]), int(args[2]))


if __name__ == "__main__":
    main(sys.argv[1:])
