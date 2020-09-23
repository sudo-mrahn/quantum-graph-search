"""
module to create simulation parameters from graphs

created by Alex Ahn
alex.song.ahn@gmail.com
Temple University
Department of Mathematics
"""

import copy
import numpy as np
from graph.attributes import degrees_of, is_connected


def count_edges(adj):
    """
    returns number of edges in an undirected graph represented by adj
    """
    return int(np.around(np.count_nonzero(adj) / 2))


def fill(tree, tot):
    """
    given tree graph, add edges randomly so that the graph has tot edges.

    this is an in-place function; it doesn't return any values.
    """

    n_edges = count_edges(tree)
    add = tot - n_edges
    if add <= 0:
        print("already have that many edges")
    elif (len(tree) * (len(tree) - 1) / 2) < tot:
        print("impossible to assign that many")
    else:
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
        for k in range(len(chosen)):
            tree[options[k, 0], options[k, 1]] = 1
            tree[options[k, 1], options[k, 0]] = 1


def pick_nodes(adj_mat, setting, num):
    """
    pick node samples
    num should be int for setting in ['l', 'h']
    and list for setting == 'm'

    returns 1-d array
    """
    degrees = degrees_of(adj_mat)
    error_message = "invalid input for pick_nodes"
    if setting in ("low", "l"):
        if isinstance(num, int):
            nodes = np.argwhere(degrees <= num)[:, 0]
        else:
            print(error_message)
    elif setting in ("medium", "med", "m"):
        if isinstance(num, list):
            nodes = np.argwhere(np.isin(degrees, num))[:, 0]
        else:
            print(error_message)
    elif setting in ("high", "h"):
        if isinstance(num, int):
            nodes = np.argwhere(degrees >= num)[:, 0]
        else:
            print(error_message)
    else:
        print(error_message)
    return nodes


def bye_nb(adj, ref, n_bye):
    """
    removes edges from the neighborhood of a given vertex.
    returns the updated adjacency matrix.

    inputs
    adj:        adjacency matrix of graph to be shrunk
    n_bye:       number of edges to delete


    fixed parameters
    ref:        reference node wrt which edges are deleted
    """

    mat = copy.deepcopy(adj)
    neighbors = np.nonzero(mat[:, ref])[0]  # current neighbors
    if len(neighbors) <= n_bye:
        # print("WARNING: cannot remove all neighbors!")
        return mat

    bye_list = np.random.choice(neighbors, n_bye, replace=False)  # to delete
    neighbors = np.setdiff1d(neighbors, bye_list, assume_unique=True)
    # neighbors after edge deletion

    for bye in bye_list:
        mat[ref, bye] = 0
        mat[bye, ref] = 0

    return mat


def bye_st(adj, n_bye):
    """
    removes some edges that do not contain vertex 0 from the given graph.


    bye_st tries to delete n_bye edges in the nbhd of each non-marked vertex
    without deleting any edges that connect to the marked vertex.

    if a node has n_bye or less neighbors, by the default behavior of bye_nb it
    throws a warning and doesn't delete any from that node in that iteration.
    However, those edges can still be deleted in later iterations on other
    nodes with larger neighborhoods.

    Therefore in ANY call to this function, it is possible that:
        a node ends up with only 1 neighbor, the marked vertex
        a node loses more neighbors than n_bye
        a node does not lose any neighbors
            (if it has <= n_bye neighbors, and its edges are never picked in
            other iterations)

    The total number of edges removed is <= (len(adj) - 1) * n_bye


    returns adjacency matrix of shrunk graph.


    adj:        adjacency matrix of graph to be shrunk
    n_bye:       number of edges to delete
    """

    mat = adj[1:, 1:]  # assume marked = 0
    for j in range(len(mat)):
        mat = bye_nb(mat, j, n_bye)
    return np.block([[0, np.ones((1, len(mat)))],
                     [np.ones((len(mat), 1)), mat]])


def bye_cp(adj, r_out, r_in):
    """
    removes r_out edges from outside the marked nbhd, and r_in edges from
    inside the marked nbhd.

    it is assumed that marked=0.

    returns updated adjacency matrix.
    """
    marked = 0

    mat = copy.deepcopy(adj)
    mat = bye_nb(mat, marked, r_in)
    temp = bye_st(mat, r_out)
    while not is_connected(temp):
        temp = bye_st(mat, r_out)
    return temp


# main method
if __name__ == "__main__":
    print("yayyy!!!")
