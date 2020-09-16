"""
module to support the quantum search modules.
this contains some useful functions.

created by Alex Ahn
alex.song.ahn@gmail.com
Temple University
Department of Mathematics
"""

import numpy as np
from graph.attributes import degrees_of


def initialize(adj, mode=None, marked=None):
    """
    define an initial state: given adj matrix and marked node,
    returns the initial state (2-d array) of the given mode (nbhd or loop).

    adj:        adjacency matrix of graph
    marked:     index of marked vertex
    mode:       type of initialization:
        l:      put amplitude 1 in a self-loop at marked. this is not in the
                Hilbert space for unitary operators.
        n:      uniform distribution on the neighborhood of marked
        u:      uniform distribution on the Hilbert space, i.e. all directed
                edges.

    if marked and mode are not provided, then return the uniform distribution
    on all edges, i.e. same as mode='u'
    """

    degrees = degrees_of(adj)
    state = np.zeros_like(adj.astype(float))
    if mode is not None:
        if marked is not None:
            if mode in ["loop", "l"]:
                state[marked, marked] = 1
                # this is only in the augmented Hilbert space
            if mode in ["nbhd", "n"]:
                alpha = 1 / np.sqrt(degrees[marked])
                state[:, marked] = alpha * adj[:, marked]
                # this is in the Hilbert space
                # it is not symmetric
        if mode in ["uniform", "u", "unif"]:
            alpha = 1 / np.sqrt(np.count_nonzero(adj))
            state = alpha * adj

    # this should cover the case where only adj is provided
    else:
        alpha = 1 / np.sqrt(np.count_nonzero(adj))
        state = alpha * adj

    if np.max(state) == np.min(state):
        print("something may have gone wrong. double check results.")
    return state


def modulus(state):
    """
    return the modulus of the state
    """
    return np.sum(state**2)


def search_times(prob, prop):
    """
    compute search times. input is either a list of integers, or a 2-d array of
    dimensions T by S, where T is total timesteps and S is the total number of
    simulations (samples) run.

    returns either an int or a 1-d array of integers, i.e. either a search time
    or a vector of search times corresponding to each QS simulation
    """

    time_to_success = None
    if type(prob) is type(np.array([])):  # ignore E721. we do want type
        ncols = len(prob[0, :])
        max_prob = np.zeros(ncols)
        time_to_success = np.zeros(ncols)

        # iterate through the samples (columns) of prob
        for j in range(ncols):
            max_prob[j] = np.max(prob[:, j])

            # find the hitting time of p*max_prob[i]!
            for i in range(len(prob[:, j])):
                if prob[i, j] >= prop * max_prob[j]:
                    break
                time_to_success[j] += 1
    if type(prob) is type([]):  # ignore E721
        max_prob = max(prob)
        time_to_success = 0
        for _, elem in enumerate(prob):
            if elem >= prop * max_prob:
                break
            time_to_success += 1

    return time_to_success
