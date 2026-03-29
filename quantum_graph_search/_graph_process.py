"""Graph-transformation helpers used to build simulation variants."""

import copy
import random

import numpy as np

from quantum_graph_search._graph_attributes import degrees_of, is_connected


def count_edges(adj):
    """
    Return the number of edges in an undirected graph represented by ``adj``.
    """

    return int(np.around(np.count_nonzero(adj) / 2))


def fill_in(adj, n_add):
    """
    Randomly add ``n_add`` edges to the neighborhood of vertex 0.
    """

    if n_add < 0:
        raise ValueError("n_add must be non-negative")

    mat = copy.deepcopy(adj)
    edge_pool = np.nonzero(adj[0, :] == 0)[0][1:]
    if n_add > len(edge_pool):
        raise ValueError("cannot add more neighborhood edges than are available")

    chosen_ones = np.random.choice(edge_pool, n_add, replace=False)
    for i in chosen_ones:
        mat[0, i] = 1
        mat[i, 0] = 1
    return mat


def fill_out(adj, n_add):
    """
    Randomly add ``n_add`` edges to the graph with the marked node removed.
    """

    if n_add < 0:
        raise ValueError("n_add must be non-negative")

    subgraph = copy.deepcopy(adj[1:, 1:])
    temp = np.nonzero(np.triu(subgraph == 0, 1))
    edge_pool = [list(elem) for elem in list(zip(temp[0], temp[1]))]
    if n_add > len(edge_pool):
        raise ValueError("cannot add more non-marked edges than are available")

    random.shuffle(edge_pool)
    for pick in edge_pool[:n_add]:
        subgraph[pick[0], pick[1]] = 1
        subgraph[pick[1], pick[0]] = 1

    return np.block(
        [
            [0, adj[0, 1:]],
            [adj[1:, 0].reshape(len(subgraph), 1), subgraph],
        ]
    )


def fill_out_upto(adj, total):
    """
    Add edges outside the marked node until the subgraph reaches ``total``.
    """

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
    Add edges randomly so the graph has ``tot`` total edges in place.
    """

    n_edges = count_edges(tree)
    add = tot - n_edges
    if add <= 0:
        raise ValueError("graph already has at least that many edges")
    if (len(tree) * (len(tree) - 1) / 2) < tot:
        raise ValueError("cannot assign that many edges to the graph")

    zeros = np.transpose(np.nonzero(tree == 0))
    options = []
    for _, zero in enumerate(zeros):
        if zero[0] < zero[1]:
            options.append(zero)
    options = np.array(options)
    chosen = np.random.choice(len(options), add, replace=False)
    for option_index in chosen:
        tree[options[option_index, 0], options[option_index, 1]] = 1
        tree[options[option_index, 1], options[option_index, 0]] = 1

    return tree


def fill_to_total_edges(adj, total):
    """
    Return a copy of ``adj`` with edges added until the graph has ``total``.
    """

    new_adj = copy.deepcopy(adj)
    return fill_inplace(new_adj, total)


def fill(tree, tot):
    """
    Backward-compatible alias for ``fill_inplace``.
    """

    return fill_inplace(tree, tot)


def pick_low_degree_nodes(adj_mat, max_degree):
    """
    Return nodes whose degree is at most ``max_degree``.
    """

    if not isinstance(max_degree, int):
        raise TypeError("max_degree must be an int")

    degrees = degrees_of(adj_mat)
    return np.argwhere(degrees <= max_degree)[:, 0]


def pick_medium_degree_nodes(adj_mat, allowed_degrees):
    """
    Return nodes whose degree is one of the values in ``allowed_degrees``.
    """

    if not isinstance(allowed_degrees, list):
        raise TypeError("allowed_degrees must be a list of ints")

    degrees = degrees_of(adj_mat)
    return np.argwhere(np.isin(degrees, allowed_degrees))[:, 0]


def pick_high_degree_nodes(adj_mat, min_degree):
    """
    Return nodes whose degree is at least ``min_degree``.
    """

    if not isinstance(min_degree, int):
        raise TypeError("min_degree must be an int")

    degrees = degrees_of(adj_mat)
    return np.argwhere(degrees >= min_degree)[:, 0]


def pick_nodes(adj_mat, setting, num):
    """
    Return node samples chosen by degree bucket.
    """

    if setting in ("low", "l"):
        return pick_low_degree_nodes(adj_mat, num)
    if setting in ("medium", "med", "m"):
        return pick_medium_degree_nodes(adj_mat, num)
    if setting in ("high", "h"):
        return pick_high_degree_nodes(adj_mat, num)

    raise ValueError("setting must be one of 'low', 'medium', or 'high'")


def remove_neighborhood_edges(adj, ref, n_bye):
    """
    Remove ``n_bye`` edges from the neighborhood of the reference vertex.
    """

    if n_bye < 0:
        raise ValueError("n_bye must be non-negative")

    mat = copy.deepcopy(adj)
    neighbors = np.nonzero(mat[:, ref])[0]
    if len(neighbors) <= n_bye:
        return mat

    bye_list = np.random.choice(neighbors, n_bye, replace=False)
    for bye in bye_list:
        mat[ref, bye] = 0
        mat[bye, ref] = 0

    return mat


def remove_non_marked_edges(adj, n_bye):
    """
    Remove edges outside the marked neighborhood while preserving edges to 0.
    """

    mat = adj[1:, 1:]
    for j in range(len(mat)):
        mat = remove_neighborhood_edges(mat, j, n_bye)
    return np.block(
        [
            [0, np.ones((1, len(mat)))],
            [np.ones((len(mat), 1)), mat],
        ]
    )


def remove_inside_outside_edges(adj, r_out, r_in):
    """
    Remove edges both inside and outside the marked neighborhood.
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
    Backward-compatible alias for ``remove_neighborhood_edges``.
    """

    return remove_neighborhood_edges(adj, ref, n_bye)


def bye_st(adj, n_bye):
    """
    Backward-compatible alias for ``remove_non_marked_edges``.
    """

    return remove_non_marked_edges(adj, n_bye)


def bye_cp(adj, r_out, r_in):
    """
    Backward-compatible alias for ``remove_inside_outside_edges``.
    """

    return remove_inside_outside_edges(adj, r_out, r_in)
