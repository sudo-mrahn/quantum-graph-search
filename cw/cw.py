"""
module to run a classical walk on a given graph G

created by Alex Ahn
alex.song.ahn@gmail.com

last edited Sep 5 2020
Temple University
Deparment of Mathematics

dependencies:
    numpy, networkx, matplotlib, python3.8
    graph (custom module. ask Alex for details)

usage:
$ python cw.py graph_size starting_node total_iterations

all input parameters are integers.
"""

import sys
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import graph.make


def step(adj, node):
    """
    next step in the random walk from given node.
    returns int of next node index.

    adj:    adjacency matrix of graph
    node:   current node position
    """
    return np.random.choice(np.nonzero(adj[:, node])[0], 1)[0]


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


# main ------------------------------------------------------------------------
def main(args):
    """
    test what I wrote up there

    seems to work fine on spiked cyclic graphs! Try barabasi: also looks good.
    """

    temp_adj = graph.make.cycle(int(args[0]), 6)
    # cyclic graph of given size with 6 spikes

    # temp_adj = graph.make.barabasi(int(args[0]), 3)  # parse input as int
    path = walk(temp_adj, int(args[1]), int(args[2]))
    print(path)
    temp_g = nx.Graph(temp_adj)
    nx.draw(temp_g, with_labels=True)
    print("random walk on a graph of size " + args[0])
    plt.show()


if __name__ == "__main__":
    main(sys.argv[1:])
