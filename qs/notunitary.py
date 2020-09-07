"""
module to run a modified, non-unitary version of the flip-flop Grover search on
a given graph G

created by Alex Ahn
alex.song.ahn@gmail.com
last edited Sep 4 2020
Temple University
Department of Mathematics
"""

import numpy as np
from graph.attributes import degrees_of


# uncorrected operators
# i.e. these are not unitary.
def oracle(state, marked_node):
    """
    oracle operator
    """
    mat = state.astype(float)
    mat[:, marked_node] = -1 * mat[:, marked_node]
    return mat


def coin(state, deg, adj):
    """
    NOTE: this operator acts on an augmented Hilbert space of all possible node
    pair vectors, not the limited Hilbert space of directed edges specified by
    adj.

    state: quantum state of the graph, represented as a matrix in the shape of
    an adjacency matrix with coefficients of the vectors in the Hilbert space
    as entries
    deg: vector of node degrees
    adj: adjacency matrix of the graph. this may or may NOT be equivalent to
    the state matrix with nonzero entries replaced by 1.
    """

    new_state = np.zeros_like(state)
    current_size = len(new_state[:, 0])

    for i in range(current_size):
        # sum coefficients of vectors
        ampl_sum = np.sum(state[:, i])
        if deg[i] == 0:
            print("deg[i]: " + str(deg[i]))
            print("there is your problem")
        new_state[:, i] = (2 * ampl_sum / deg[i]) * adj[:, i]

    new_state = new_state - state

    return new_state


def shift(state):
    """
    shift operator
    """
    return np.transpose(state)


def qsearch(state, deg, adj, marked_node, t_1):
    """
    one iteration of the quantum search
    """
    new_state = oracle(state, marked_node)
    for _ in range(t_1):
        new_state = shift(coin(new_state, deg, adj))

    return new_state


def prob(state, vertex):
    """
    probability at given vertex
    """
    neighborhood = state[:, vertex]
    return np.sum(neighborhood**2)


def sample(adj_mat, node_indices, maxss, total_steps, t_1):
    """
    run qs on given sample of nodes
    given adjacency matrix adj_mat, 1-d array of indices node_indices
    returns prob_at_marked
    """
    # initialize
    alpha = 1 / np.sqrt(
        np.count_nonzero(adj_mat))  # uniform initial distribution
    degrees = degrees_of(adj_mat)
    #    global m

    nsamples = min(maxss, len(node_indices))
    # this is a 1-d array
    prob_at_marked = np.zeros(
        (total_steps + 1, nsamples))  # t+1 for initial state + t timesteps

    progress = 0
    # iterate through nodes in node_indices
    for marked_node in node_indices[:nsamples].astype(int):
        progress += 1

        # uniform initial distribution
        state = alpha * adj_mat  # re-initialize state for each node (duh)
        prob_at_marked[0, progress - 1] = prob(state, marked_node)

        # run QS for node m
        for i in range(1, total_steps + 1):
            state = qsearch(state, degrees, adj_mat, marked_node,
                            t_1)  # run one step of the qs
            # retrieve probabilities
            prob_at_marked[i, progress - 1] = prob(state, marked_node)

        # progress bar
        if progress % (int(np.round(nsamples / 10))) == 0:
            print(str(np.round(100 * progress / nsamples, 1)) + "% complete")

    return prob_at_marked
