"""Classical random walk utilities on dense adjacency matrices."""

import sys
import numpy as np
from graph import cycle


def step(adj, node):
    """
    next step in the random walk from given node.
    returns int of next node index.

    adj:    adjacency matrix of graph
    node:   current node position
    """
    neighbors = np.nonzero(adj[:, node])[0]
    if len(neighbors) == 0:
        raise ValueError("cannot take a walk step from an isolated vertex")
    return np.random.choice(neighbors, 1)[0]


def walk(adj, start, duration):
    """
    random walk on a graph for a fixed duration.
    returns a list of nodes traversed.

    adj:        adjacency matrix of graph
    start:      vertex at time 0
    duration:   total number of iterations to be run

    note that each neighbor is equally likely to be chosen at the next timestep
    """

    path = [start]
    for k in range(duration):
        path.append(step(adj, path[k]))

    return path


def return_times(adj, start, n_samples):
    """
    return time of a random walk on a graph.
    returns a list of return times.

    adj:        adjacency matrix of graph
    start:      vertex at time 0
    n_samples:  number of random walks to sample
    """

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
    run and plot a classical walk demo on a spiked cycle graph.
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
