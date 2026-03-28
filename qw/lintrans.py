"""Linear-transformation constructions for quantum-walk operators."""

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
    if operator not in ["coin", "c"]:
        raise ValueError("operator must be 'coin' or 'c'")
    if method not in ["np.block", "scipy.linalg", "scipy.sparse"]:
        raise ValueError(
            "method must be one of 'np.block', 'scipy.linalg', or 'scipy.sparse'"
        )

    degrees = degrees_of(adj_mat)
    if np.any(degrees == 0):
        raise ValueError(
            "coin linear transformation is undefined on graphs with isolated vertices"
        )

    inv_degrees = 1 / degrees  # coefficient for each block
    lt_block = inv_degrees[0] * get_colblock(adj_mat, 0)  # first block

    if method == "np.block":
        for j in range(1, graph_size):
            lt_block = np.block([
                [lt_block, np.zeros((len(lt_block), graph_size))],
                [
                    np.zeros((graph_size, len(lt_block))),
                    inv_degrees[j] * get_colblock(adj_mat, j),
                ],
            ])
    elif method == "scipy.linalg":
        for j in range(1, graph_size):
            lt_block = block_diag(lt_block, inv_degrees[j] * get_colblock(adj_mat, j))
    else:
        lt_block = coo_matrix(lt_block)
        for j in range(1, graph_size):
            lt_block = sparse_block_diag((
                lt_block,
                coo_matrix(inv_degrees[j] * get_colblock(adj_mat, j)),
            ))
        lt_block = lt_block.toarray()

    return 2 * lt_block - np.eye(dim)
