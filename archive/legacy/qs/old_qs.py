"""
module to run a flip-flop Grover search on a given graph G
the Hilbert space on which the operators act is that of directed edges of G

created by Alex Ahn
last edited Aug 26 2020
Temple University
Department of Mathematics
"""

import numpy as np
from graph.attributes import degrees_of


# section 1 -----------------------------------------------------------------
# corrected operators
def cor_oracle(state, marked_node, adj):
    """
    corrected oracle operator
    """
    state[:, marked_node] -= 2 * adj[:, marked_node] * state[:, marked_node]
    return state


def cor_coin(state, deg, adj):
    """
    corrected version of the coin operator

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


def cor_shift(state, adj):
    """
    corrected shift operator
    """
    return (state * adj).T


def cor_qsearch(state, deg, adj, marked_node, t_1):
    """
    one iteration of the quantum search
    """
    new_state = cor_oracle(state, marked_node, adj)
    for _ in range(t_1):
        new_state = cor_shift(cor_coin(new_state, deg, adj), adj)

    return new_state


def cor_prob(state, marked, adj):
    """
    corrected probability at given vertex
    """
    return np.sum((state[:, marked] * adj[:, marked])**2)


def cor_sample(adj_mat, node_indices, maxss, total_steps, t_1):
    """
    **corrected version**

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
        prob_at_marked[0, progress - 1] = cor_prob(state, marked_node, adj_mat)

        # run QS for node m
        for i in range(1, total_steps + 1):
            state = cor_qsearch(state, degrees, adj_mat, marked_node,
                                t_1)  # run one step of the qs
            # retrieve probabilities
            prob_at_marked[i, progress - 1] = cor_prob(state, marked_node,
                                                       adj_mat)

        # progress bar
        if progress % (int(np.round(nsamples / 10))) == 0:
            print(str(np.round(100 * progress / nsamples, 1)) + "% complete")

    return prob_at_marked


# section 2 -----------------------------------------------------------------
# uncorrected operators
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


# section 3 -----------------------------------------------------------------
# uncorrected operators


# here I try to improve the runtime of the coin operator
# note that this was attempted on the old coin operator
# i.e. the incorrectly implemented coin operator.
def new_coin_v1(state, deg, adj):
    """
    let's try to parallelize coin oper
    """
    diag_1 = np.zeros_like(state)
    diag_2 = np.zeros_like(state)
    np.fill_diagonal(diag_1, 2.0 / deg)
    np.fill_diagonal(diag_2, np.dot(np.ones((1, len(state))), state))
    new_state = np.dot(adj, np.dot(diag_1, diag_2))
    return new_state - state


# def coin(state, deg, adj):
#     """
#     temp copy of new_coin_v2
#     for testing purposes
#     """
#     diag_1 = np.zeros_like(state)
#     diag_2 = np.zeros_like(state)
#     np.fill_diagonal(diag_1, 2.0 / deg)
#     np.fill_diagonal(diag_2, np.dot(np.ones((1, len(state))), state))
#     new_state = np.dot(
#         adj, np.multiply(np.diag(diag_1)[:, None],
#                          np.diag(diag_2)[:, None]))
#     return new_state - state


def new_coin_v2(state, deg, adj):
    """
    let's try to parallelize coin oper

    may be faster if the last (outermost) broadcasting step is not done
    """
    diag_1 = np.zeros_like(state)
    diag_2 = np.zeros_like(state)
    np.fill_diagonal(diag_1, 2.0 / deg)
    np.fill_diagonal(diag_2, np.dot(np.ones((1, len(state))), state))
    new_state = np.dot(
        adj, np.multiply(np.diag(diag_1)[:, None],
                         np.diag(diag_2)[:, None]))
    return new_state - state


def new_coin_v3(state, deg, adj):
    """
    let's try to parallelize coin oper

    may be faster if the last (outermost) broadcasting step is not done
    """
    diag_1 = np.zeros_like(state)
    diag_2 = np.zeros_like(state)
    np.fill_diagonal(diag_1, 2.0 / deg)
    np.fill_diagonal(diag_2, np.dot(np.ones((1, len(state))), state))
    new_state = np.multiply(
        adj,
        np.diag(np.multiply(
            np.diag(diag_1)[:, None],
            np.diag(diag_2)[:, None]))[:, None],
    )
    return new_state - state


# section 4 -----------------------------------------------------------------
# some other useful functions


def initialize(adj, marked, mode):
    """
    define an initial state: given adj matrix and marked node,
    return initial state of the given mode (nbhd or loop).
    """
    degrees = degrees_of(adj)
    state = np.zeros_like(adj.astype(float))
    if mode in ["loop", "l"]:
        state[marked, marked] = 1  # this is only in the augmented Hilbert sp
    if mode in ["nbhd", "n"]:
        alpha = 1 / np.sqrt(degrees[marked])
        state[:, marked] = alpha * adj[:, marked]  # this is in the Hilbert sp

    return state


def modulus(state):
    """
    return the modulus of the state
    """
    return np.sum(state**2)


def search_times(prob_matrix, prop):
    """
    compute search times. input is T by S, where T is total timesteps and S is
    total number of simulations (samples) run.

    returns a vector of search times corresponding to each QS simulation
    """
    ncols = len(prob_matrix[0, :])
    max_prob_matrix = np.zeros(ncols)
    time_to_success = np.zeros(ncols)

    # iterate through the samples (columns) of prob_matrix
    for j in range(ncols):
        max_prob_matrix[j] = np.max(prob_matrix[:, j])

        # find the hitting time of p*max_prob_matrix[i]!
        for i in range(len(prob_matrix[:, j])):
            if prob_matrix[i, j] >= prop * max_prob_matrix[j]:
                break
            time_to_success[j] += 1

    return time_to_success
