"""
module to create simulation parameters from graphs

created by Alex Ahn
alex.song.ahn@gmail.com

last edited Sep 7 2020
Temple University
Department of Mathematics
"""

import copy
import numpy as np
from graph.attributes import degrees_of


def pick_nodes(adj_mat, setting, num):
    """
    pick node samples
    num should be int for setting in ['l', 'h']
    and list for setting == 'm'
    """
    degrees = degrees_of(adj_mat)
    error_message = "invalid input for pick_nodes"
    if setting in ("low", "l"):
        if isinstance(num, int):
            nodes = np.argwhere(degrees <= num)[:, 0]
        else:
            print(error_message)
    elif setting in ("medium", "m"):
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
        print("WARNING: cannot remove all neighbors!")
        print("It is not good to isolate yourself, you know.")
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
    shrinks graph with respect to the reference vertex 0,
    returns adjacency matrix of shrunk graph.

    adj:        adjacency matrix of graph to be shrunk
    n_bye:       number of edges to delete
    """

    mat = adj[1:, 1:]  # assume marked = 0
    for j in range(len(mat)):
        mat = bye_nb(mat, j, n_bye)
    return np.block([[0, np.ones((1, len(mat)))],
                     [np.ones((len(mat), 1)), mat]])


def bye_ev(adj, n_bye):
    """
    shrinks graph uniformly*
    returns adjacency matrix of shrunk graph.
    """
    mat = copy.deepcopy(adj)

    return mat


# main method
if __name__ == "__main__":
    print("yayyy!!!")
