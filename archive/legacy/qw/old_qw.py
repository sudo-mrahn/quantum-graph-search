"""
module to run the Grover walk on a given graph G
the Hilbert space on which the operators act is that of directed edges of G

created by Alex Ahn
last edited Aug 25 2020
Temple University
Department of Mathematics
"""

import numpy as np
from scipy.sparse.csgraph import shortest_path
from scipy.linalg import block_diag
from scipy.sparse import coo_matrix
from scipy.sparse import block_diag as sparse_block_diag
import qs
from qs import coin, shift, degrees_of, prob


def cor_expected_dist(state, node, distances, adj):
    """
    **corrected version**

    mean distance of state wrt given node
    returns a real number
    """
    r_t = 0
    for vertex in range(len(state[:, 0])):
        r_t += distances[vertex, node] * qs.cor_prob(state, vertex, adj)
    return r_t


def cor_mean_square_dist(state, marked, distances, adj):
    """
    **corrected version**

    mean square distance of state from given node
    returns a real number
    """
    square_dist = np.square(distances)
    msd = 0
    for node in range(len(state)):
        msd += square_dist[node, marked] * qs.cor_prob(state, node, adj)
    return msd


# run 1 step of quantum walk
def cor_qwalk(state, deg, adj):
    """
    **corrected version**

    run 1 step of qw
    """
    return qs.cor_shift(qs.cor_coin(state, deg, adj), adj)


def cor_sample_r(adj_mat, marked_node_indices, initial, maxss, total_steps):
    """
    **corrected version**

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
        mean_distance[0, progress - 1] = cor_expected_dist(
            state, marked, distances, adj_mat)

        # run QW for node m
        for i in range(1, total_steps + 1):
            state = cor_qwalk(state, degrees,
                              adj_mat)  # run one step of the qw
            # retrieve mean dist
            mean_distance[i, progress - 1] = cor_expected_dist(
                state, marked, distances, adj_mat)

        # progress bar
        if progress % (int(np.round(nsamples / 10))) == 0:
            print(str(np.round(100 * progress / nsamples, 1)) + "% complete")

    return mean_distance


def cor_sample_v(adj_mat, marked_node_indices, initial, maxss, total_steps):
    """
    **corrected version**

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
        mean_distance[0, progress - 1] = cor_mean_square_dist(
            state, marked, distances, adj_mat)

        # run QW for node m
        for i in range(1, total_steps + 1):
            state = cor_qwalk(state, degrees,
                              adj_mat)  # run one step of the qw
            # retrieve mean dist
            mean_distance[i, progress - 1] = cor_mean_square_dist(
                state, marked, distances, adj_mat)

        # progress bar
        if progress % (int(np.round(nsamples / 10))) == 0:
            print(str(np.round(100 * progress / nsamples, 1)) + "% complete")

    return mean_distance


def check_symmetric(matrix):
    """
    just a quick function to check if a given matrix is approximately symmetric
    """
    return np.all(np.abs(matrix - matrix.T) < 1e-8)


def find_distances(adj_mat):
    """
    quick function to retrieve matrix of distances between vertices
    """
    return shortest_path(adj_mat, directed=False, unweighted=True)


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


# ----------------------------------------------------------------------------
# linear transformation representation of the qw operators


def get_colblock(adj_mat, col):
    """
    to be used in the get_lt function
    returns a matrix like adj_mat, except
    every column is column col
    """
    # not sure if there is a better way to do this
    # np.column_stack would require a for loop, I think

    return np.array([adj_mat[:, col] for _ in range(len(adj_mat))]).T


def get_lt(adj_mat, operator, method):
    """
    returns the n^2 by n^2 matrix that represents the linear transformation
    specified by the given operator
    """

    dim, graph_size = len(adj_mat)**2, len(adj_mat)
    lt_block = []
    if operator in ["coin", "c"]:
        inv_degrees = 1 / degrees_of(adj_mat)  # coefficient for each block
        lt_block = inv_degrees[0] * get_colblock(adj_mat, 0)  # first block

        # build block diagonal matrix
        if method == "np.block":
            for j in range(1, graph_size):
                lt_block = np.block([
                    [lt_block, np.zeros((len(lt_block), graph_size))],
                    [
                        np.zeros((graph_size, len(lt_block))),
                        inv_degrees[j] * get_colblock(adj_mat, j),
                    ],
                ])
        if method == "scipy.linalg":
            for j in range(1, graph_size):
                lt_block = block_diag(
                    lt_block, inv_degrees[j] * get_colblock(adj_mat, j))
        if method == "scipy.sparse":
            lt_block = coo_matrix(lt_block)
            for j in range(1, graph_size):
                lt_block = sparse_block_diag((
                    lt_block,
                    coo_matrix(inv_degrees[j] * get_colblock(adj_mat, j)),
                ))
            lt_block = lt_block.toarray()

        return 2 * lt_block - np.eye(dim)
    return print("invalid operator option")
