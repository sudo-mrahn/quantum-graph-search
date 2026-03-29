"""Linear-transformation constructions for quantum-walk operators."""

import numpy as np
from scipy.linalg import block_diag
from scipy.sparse import coo_matrix
from scipy.sparse import block_diag as sparse_block_diag

from quantum_graph_search._graph_attributes import degrees_of
from quantum_graph_search._validation import require_square_array


def get_colblock(adj_mat, col):
    """
    Return a matrix like ``adj_mat`` whose columns are all column ``col``.
    """

    return np.array([adj_mat[:, col] for _ in range(len(adj_mat))]).T


def get_lt(adj_mat, operator, method):
    """
    Return the matrix representation of the requested coin operator.
    """

    adj_mat = require_square_array(adj_mat, name="adj_mat")
    dim, graph_size = len(adj_mat) ** 2, len(adj_mat)
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

    inv_degrees = 1 / degrees
    lt_block = inv_degrees[0] * get_colblock(adj_mat, 0)

    if method == "np.block":
        for j in range(1, graph_size):
            lt_block = np.block(
                [
                    [lt_block, np.zeros((len(lt_block), graph_size))],
                    [
                        np.zeros((graph_size, len(lt_block))),
                        inv_degrees[j] * get_colblock(adj_mat, j),
                    ],
                ]
            )
    elif method == "scipy.linalg":
        for j in range(1, graph_size):
            lt_block = block_diag(lt_block, inv_degrees[j] * get_colblock(adj_mat, j))
    else:
        lt_block = coo_matrix(lt_block)
        for j in range(1, graph_size):
            lt_block = sparse_block_diag(
                (
                    lt_block,
                    coo_matrix(inv_degrees[j] * get_colblock(adj_mat, j)),
                )
            )
        lt_block = lt_block.toarray()

    return 2 * lt_block - np.eye(dim)
