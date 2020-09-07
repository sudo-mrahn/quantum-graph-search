"""
module to run a flip-flop Grover search on a given graph G

created by Alex Ahn
alex.song.ahn@gmail.com

last edited Sep 5 2020
Temple University
Department of Mathematics
"""

import numpy as np
from graph.attributes import degrees_of
from qs.process import initialize


# corrected operators
# i.e. these are unitary.
def oracle(state, marked_node, adj):
    """
    unitary oracle operator
    """
    state[:, marked_node] -= 2 * adj[:, marked_node] * state[:, marked_node]
    return state


def coin(state, deg, adj):
    """
    unitary version of the coin operator

    i.e. the Hilbert space acted on by this function is NOT the augmented
    Hilbert space of the directed edges of the completion of the graph
    represented by the adjacency matrix input.

    rather, it is the proper Hilbert space of directed edges represented in adj
    """

    for i in range(len(adj)):
        # sum coefficients of vectors
        ampl_sum = np.dot(adj[:, i], state[:, i])
        state[:, i] -= (2 * ampl_sum / deg[i]) * adj[:, i]

    return -1 * state


def shift(state, adj):
    """
    unitary shift operator
    """
    return (state * adj).T


def qsearch(state, deg, adj, marked_node, t_1):
    """
    one iteration of the quantum search
    returns a new quantum state after applying the qs operator

    state: input quantum state in the form of a 2-d array
    deg: 1-d array of degrees of the vertex identified with the array index
    adj: adjacency matrix of the graph
    marked_node: index of marked vertex
    t_1: number of times to apply quantum walk operator after each oracle query
    """

    new_state = oracle(state, marked_node, adj)
    for _ in range(t_1):
        new_state = shift(coin(new_state, deg, adj), adj)

    return new_state


def simulate(adj, marked, t_1, stop):
    """
    many iterations of the quantum search.
    returns an array (list) of probabilities at the marked vertex.

    stop: total number of qs iterations
    """

    deg = degrees_of(adj)
    pr_marked = []
    state = initialize(adj)  # uniform distribution initial state

    for _ in range(stop + 1):
        pr_marked.append(prob(state, marked, adj))
        state = qsearch(state, deg, adj, marked, t_1)
    return pr_marked


def prob(state, marked, adj):
    """
    corrected probability at given vertex
    """
    return np.sum((state[:, marked] * adj[:, marked])**2)


# this is some old code
# should use a list object instead of a np array for prob_at_marked
def sample(adj_mat, node_indices, maxss, total_steps, t_1):
    """
    **unitary version**

    run qs on given sample of nodes
    given adjacency matrix adj_mat, 1-d array of indices node_indices
    returns prob_at_marked
    """

    # initialize
    alpha = 1 / np.sqrt(
        np.count_nonzero(adj_mat))  # uniform initial distribution
    degrees = degrees_of(adj_mat)

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
        prob_at_marked[0, progress - 1] = prob(state, marked_node, adj_mat)

        # run QS for node m
        for i in range(1, total_steps + 1):
            state = qsearch(state, degrees, adj_mat, marked_node,
                            t_1)  # run one step of the qs
            # retrieve probabilities
            prob_at_marked[i, progress - 1] = prob(state, marked_node, adj_mat)

        # progress bar
        if progress % (int(np.round(nsamples / 10))) == 0:
            print(str(np.round(100 * progress / nsamples, 1)) + "% complete")

    return prob_at_marked
