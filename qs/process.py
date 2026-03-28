"""Supporting helpers for the quantum-search modules."""

import numpy as np
from graph.attributes import degrees_of


def quarterly(count, total):
    """
    display quarterly progress, measured by proportion of count / total.
    """
    if total <= 0:
        raise ValueError("total must be positive")

    interval = max(1, int(total / 4))
    if count in np.arange(interval, total + 1, interval):
        print("%.f%% complete" % (100 * count / total))


def initialize_loop_state(adj, marked):
    """
    initialize a state concentrated on a self-loop at the marked vertex.
    """

    state = np.zeros_like(adj, dtype=float)
    state[marked, marked] = 1
    return state


def initialize_neighborhood_state(adj, marked):
    """
    initialize a state uniformly over the marked vertex neighborhood.
    """

    degrees = degrees_of(adj)
    if degrees[marked] == 0:
        raise ValueError("marked vertex must have positive degree")

    state = np.zeros_like(adj, dtype=float)
    alpha = 1 / np.sqrt(degrees[marked])
    state[:, marked] = alpha * adj[:, marked]
    return state


def initialize_uniform_state(adj):
    """
    initialize a state uniformly over all directed edges.
    """

    n_edges = np.count_nonzero(adj)
    if n_edges == 0:
        raise ValueError("adjacency matrix must contain at least one edge")

    alpha = 1 / np.sqrt(n_edges)
    return alpha * adj.astype(float)


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

    if mode is None:
        return initialize_uniform_state(adj)

    if mode in ["uniform", "u", "unif"]:
        return initialize_uniform_state(adj)

    if marked is None:
        raise ValueError("marked must be provided for loop or neighborhood modes")

    if mode in ["loop", "l"]:
        return initialize_loop_state(adj, marked)
    if mode in ["nbhd", "n"]:
        return initialize_neighborhood_state(adj, marked)

    raise ValueError("mode must be one of loop, nbhd, or uniform")


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
    if isinstance(prob, np.ndarray):
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
    elif isinstance(prob, list):
        max_prob = max(prob)
        time_to_success = 0
        for _, elem in enumerate(prob):
            if elem >= prop * max_prob:
                break
            time_to_success += 1
    else:
        raise TypeError("prob must be a list or a NumPy array")

    return time_to_success
