"""
module to run a modified, non-unitary version of the flip-flop Grover walk

created by Alex Ahn
alex.song.ahn@gmail.com
Temple University
Department of Mathematics
"""

import numpy as np
from qs.process import initialize
from qs.notunitary import coin, shift, prob
from graph.attributes import find_distances, degrees_of


def expected_dist(state, node, distances):
    """
    mean distance of state wrt given node
    returns a real number
    """
    r_t = 0
    for vertex in range(len(state[:, 0])):
        r_t += distances[vertex, node] * prob(state, vertex)
    return r_t


def mean_square_dist(state, marked, distances):
    """
    mean square distance of state from given node
    returns a real number
    """
    square_dist = np.square(distances)
    msd = 0
    for node in range(len(state)):
        msd += square_dist[node, marked] * prob(state, node)
    return msd


# run 1 step of quantum walk
def qwalk(state, deg, adj):
    """
    run 1 step of qw
    """
    return shift(coin(state, deg, adj))


def get_ldists(adj, marked, l_type, stop):
    """
    simulate a quantum walk for timesteps up to 'stop' while measuring the
    localization of the quantum state wrt. the marked vertex at each step.

    returns a list of localization measures (mean distance or mean square
    distance) over all timesteps.

    note that this function usees the non-unitary quantum operators.
    """

    distances = find_distances(adj)
    degrees = degrees_of(adj)
    ldists = []
    state = initialize(adj, "loop", marked)  # initial quantum state

    for _ in range(stop + 1):
        if l_type == "md":
            ldists.append(expected_dist(state, marked, distances))
        elif l_type == "msd":
            ldists.append(mean_square_dist(state, marked, distances))
        else:
            print("\n\n ERROR: Invalid l_type argument \n\n")
            return []
        state = qwalk(state, degrees, adj)

    return ldists


# -----------------------------------------------------------------------------
# old code. probably needs to be deprecated
def sample_r(adj_mat, marked_node_indices, initial, maxss, total_steps):
    """
    run qw on given sample of nodes
    given adjacency matrix adj_mat, 1-d array of indices marked_node_indices
    returns r_t
    """
    # initialize
    distances = find_distances(adj_mat)
    degrees = degrees_of(adj_mat)
    nsamples = min(maxss, len(marked_node_indices))  # this is a 1-d array
    mean_distance = np.zeros(
        (total_steps + 1, nsamples))  # t+1 for initial state and t timesteps

    progress = 0
    # iterate through nodes in marked_node_indices
    for marked in marked_node_indices[:nsamples].astype(int):
        progress += 1
        state = np.zeros_like(adj_mat)

        # re initialize the state for each marked vertex in marked_node_indices
        if initial in ["loop", "l"]:
            state[marked, marked] = 1
        if initial in ["nbhd", "n"]:
            alpha = 1 / np.sqrt(degrees[marked])
            state[:, marked] = alpha * adj_mat[:, marked]

        # get initial mean distance
        mean_distance[0, progress - 1] = expected_dist(state, marked,
                                                       distances)

        # run QW for node m
        for i in range(1, total_steps + 1):
            state = qwalk(state, degrees, adj_mat)  # run one step of the qw
            # retrieve mean dist
            mean_distance[i, progress - 1] = expected_dist(
                state, marked, distances)

        # progress bar
        if progress % (int(np.round(nsamples / 10))) == 0:
            print(str(np.round(100 * progress / nsamples, 1)) + "% complete")

    return mean_distance


def sample_v(adj_mat, marked_node_indices, initial, maxss, total_steps):
    """
    run qw on given sample of nodes
    given adjacency matrix adj_mat, 1-d array of indices marked_node_indices
    returns v_t
    """
    # initialize
    distances = find_distances(adj_mat)
    degrees = degrees_of(adj_mat)
    nsamples = min(maxss, len(marked_node_indices))  # this is a 1-d array
    mean_distance = np.zeros(
        (total_steps + 1, nsamples))  # t+1 for initial state and t timesteps

    progress = 0
    # iterate through nodes in marked_node_indices
    for marked in marked_node_indices[:nsamples].astype(int):
        progress += 1
        state = np.zeros_like(adj_mat)

        # re initialize the state for each marked vertex in marked_node_indices
        if initial in ["loop", "l"]:
            state[marked, marked] = 1
        if initial in ["nbhd", "n"]:
            alpha = 1 / np.sqrt(degrees[marked])
            state[:, marked] = alpha * adj_mat[:, marked]

        # get initial mean distance
        mean_distance[0,
                      progress - 1] = mean_square_dist(state, marked,
                                                       distances)

        # run QW for node m
        for i in range(1, total_steps + 1):
            state = qwalk(state, degrees, adj_mat)  # run one step of the qw
            # retrieve mean dist
            mean_distance[i, progress - 1] = mean_square_dist(
                state, marked, distances)

        # progress bar
        if progress % (int(np.round(nsamples / 10))) == 0:
            print(str(np.round(100 * progress / nsamples, 1)) + "% complete")

    return mean_distance
