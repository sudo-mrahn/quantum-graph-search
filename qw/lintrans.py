"""
module to construct the linear transformation representation of the quantum
walk.

created by Alex Ahn
alex.song.ahn@gmail.com

last edited Sep 4 2020
Temple University
Department of Mathematics
"""

import numpy as np
from scipy.linalg import block_diag
from scipy.sparse import coo_matrix
from scipy.sparse import block_diag as sparse_block_diag
from graph.attributes import degrees_of

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
