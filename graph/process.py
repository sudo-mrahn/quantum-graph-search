"""Graph-transformation helpers used to build simulation variants."""

import copy
import random
import numpy as np
from graph.attributes import degrees_of, is_connected


def count_edges(adj):
    """
    returns number of edges in an undirected graph represented by adj
    """
    return int(np.around(np.count_nonzero(adj) / 2))


def fill_in(adj, n_add):
    """
    randomly add n_add edges to the nbhd of 0.

    returns the augmented adjacency matrix.
    """
    if n_add < 0:
        raise ValueError("n_add must be non-negative")

    mat = copy.deepcopy(adj)
    edge_pool = np.nonzero(adj[0, :] == 0)[0][1:]  # [1:] to exclude 0 itself
    if n_add > len(edge_pool):
        raise ValueError("cannot add more neighborhood edges than are available")

    chosen_ones = np.random.choice(edge_pool, n_add, replace=False)
    for i in chosen_ones:
        mat[0, i] = 1
        mat[i, 0] = 1
    return mat


def fill_out(adj, n_add):
    """
    assuming marked = 0, randomly add the given number of edges to the subgraph
    G - marked.

    the nbhd of 0 is not modified.

    returns the augmented adjacency matrix
    """

    if n_add < 0:
        raise ValueError("n_add must be non-negative")

    subgraph = copy.deepcopy(adj[1:, 1:])
    temp = np.nonzero(np.triu(subgraph == 0, 1))  # unique empty edge slots

    # make into a list of lists
    edge_pool = [list(elem) for elem in list(zip(temp[0], temp[1]))]
    if n_add > len(edge_pool):
        raise ValueError("cannot add more non-marked edges than are available")

    random.shuffle(edge_pool)  # shuffle the order

    # since we shuffled, randomly choosing n_add elements is same as picking
    # the first n_add elements
    for pick in edge_pool[:n_add]:
        subgraph[pick[0], pick[1]] = 1
        subgraph[pick[1], pick[0]] = 1  # add both directions

    return np.block([[0, adj[0, 1:]],
                     [adj[1:, 0].reshape(len(subgraph), 1), subgraph]])


def fill_out_upto(adj, total):
    """
    assuming marked = 0, randomly add edges to the subgraph G - marked until
    the number of edges in the subgraph is equal to 'total'.

    the nbhd of 0 is not modified.

    returns the augmented adjacency matrix.
    """

    # figure out how much more we need to add
    subgraph = copy.deepcopy(adj[1:, 1:])
    n_now = len(np.nonzero(np.triu(subgraph, 1))[0])
    n_more = total - n_now

    if n_more < 0:
        raise ValueError(
            "the subgraph already contains more edges than the requested total"
        )

    return fill_out(adj, n_more)


def fill_inplace(tree, tot):
    """
    given a graph, add edges randomly so that the graph has tot edges.

    this is an in-place function; it mutates and returns the input array.
    """

    n_edges = count_edges(tree)
    add = tot - n_edges
    if add <= 0:
        raise ValueError("graph already has at least that many edges")
    if (len(tree) * (len(tree) - 1) / 2) < tot:
        raise ValueError("cannot assign that many edges to the graph")

    zeros = np.transpose(
        np.nonzero(tree == 0)
    )  # includes the zeros at self loops, and duplicates upper and lower
    options = []
    for _, zero in enumerate(zeros):
        if zero[0] < zero[1]:
            options.append(zero)
    options = np.array(options)
    chosen = np.random.choice(
        len(options), add,
        replace=False)  # chosen edges, by their index in options
    for option_index in chosen:
        tree[options[option_index, 0], options[option_index, 1]] = 1
        tree[options[option_index, 1], options[option_index, 0]] = 1

    return tree


def fill_to_total_edges(adj, total):
    """
    return a copy of adj with edges added until the graph has total edges.
    """

    new_adj = copy.deepcopy(adj)
    return fill_inplace(new_adj, total)


def fill(tree, tot):
    """
    backward-compatible alias for fill_inplace.
    """

    return fill_inplace(tree, tot)


def pick_low_degree_nodes(adj_mat, max_degree):
    """
    return nodes whose degree is at most max_degree.
    """

    if not isinstance(max_degree, int):
        raise TypeError("max_degree must be an int")

    degrees = degrees_of(adj_mat)
    return np.argwhere(degrees <= max_degree)[:, 0]


def pick_medium_degree_nodes(adj_mat, allowed_degrees):
    """
    return nodes whose degree is one of the values in allowed_degrees.
    """

    if not isinstance(allowed_degrees, list):
        raise TypeError("allowed_degrees must be a list of ints")

    degrees = degrees_of(adj_mat)
    return np.argwhere(np.isin(degrees, allowed_degrees))[:, 0]


def pick_high_degree_nodes(adj_mat, min_degree):
    """
    return nodes whose degree is at least min_degree.
    """

    if not isinstance(min_degree, int):
        raise TypeError("min_degree must be an int")

    degrees = degrees_of(adj_mat)
    return np.argwhere(degrees >= min_degree)[:, 0]


def pick_nodes(adj_mat, setting, num):
    """
    pick node samples
    num should be int for setting in ['l', 'h']
    and list for setting == 'm'

    returns 1-d array
    """
    if setting in ("low", "l"):
        return pick_low_degree_nodes(adj_mat, num)
    elif setting in ("medium", "med", "m"):
        return pick_medium_degree_nodes(adj_mat, num)
    elif setting in ("high", "h"):
        return pick_high_degree_nodes(adj_mat, num)

    raise ValueError("setting must be one of 'low', 'medium', or 'high'")


def remove_neighborhood_edges(adj, ref, n_bye):
    """
    remove n_bye edges from the neighborhood of the reference vertex.
    """

    if n_bye < 0:
        raise ValueError("n_bye must be non-negative")

    mat = copy.deepcopy(adj)
    neighbors = np.nonzero(mat[:, ref])[0]  # current neighbors
    if len(neighbors) <= n_bye:
        return mat

    bye_list = np.random.choice(neighbors, n_bye, replace=False)  # to delete
    neighbors = np.setdiff1d(neighbors, bye_list, assume_unique=True)
    # neighbors after edge deletion

    for bye in bye_list:
        mat[ref, bye] = 0
        mat[bye, ref] = 0

    return mat


def remove_non_marked_edges(adj, n_bye):
    """
    remove edges outside the marked neighborhood while preserving edges to 0.
    """

    mat = adj[1:, 1:]  # assume marked = 0
    for j in range(len(mat)):
        mat = remove_neighborhood_edges(mat, j, n_bye)
    return np.block([[0, np.ones((1, len(mat)))],
                     [np.ones((len(mat), 1)), mat]])


def remove_inside_outside_edges(adj, r_out, r_in):
    """
    experimental helper that removes edges both inside and outside the marked
    neighborhood.

    This implementation is retained for research continuity, but its results
    were historically treated with caution.
    """

    marked = 0
    mat = copy.deepcopy(adj)
    mat = remove_neighborhood_edges(mat, marked, r_in)
    temp = remove_non_marked_edges(mat, r_out)
    while not is_connected(temp):
        temp = remove_non_marked_edges(mat, r_out)
    return temp


def bye_nb(adj, ref, n_bye):
    """
    backward-compatible alias for remove_neighborhood_edges.
    """

    return remove_neighborhood_edges(adj, ref, n_bye)


def bye_st(adj, n_bye):
    """
    backward-compatible alias for remove_non_marked_edges.
    """

    return remove_non_marked_edges(adj, n_bye)


def bye_cp(adj, r_out, r_in):
    """
    backward-compatible alias for remove_inside_outside_edges.
    """

    return remove_inside_outside_edges(adj, r_out, r_in)
