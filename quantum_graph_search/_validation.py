"""Shared validation helpers for canonical graph and walk modules."""

import numpy as np


def require_square_array(matrix, *, name="matrix"):
    """
    Coerce ``matrix`` to a NumPy array and ensure it is square.
    """

    array = np.asarray(matrix)
    if array.ndim != 2 or array.shape[0] != array.shape[1]:
        raise ValueError(f"{name} must be a square 2-d array")
    return array


def require_int(name, value, *, minimum=None):
    """
    Validate integer-valued arguments.
    """

    if not isinstance(value, (int, np.integer)):
        raise TypeError(f"{name} must be an integer")
    value = int(value)
    if minimum is not None and value < minimum:
        raise ValueError(f"{name} must be at least {minimum}")
    return value


def require_probability(name, value):
    """
    Validate probability-valued arguments.
    """

    if not isinstance(value, (int, float, np.integer, np.floating)):
        raise TypeError(f"{name} must be a real number")
    value = float(value)
    if not 0 <= value <= 1:
        raise ValueError(f"{name} must be between 0 and 1")
    return value


def require_vertex_index(adj, vertex, *, name="vertex"):
    """
    Validate that ``vertex`` indexes a row/column in ``adj``.
    """

    matrix = require_square_array(adj, name="adj")
    vertex = require_int(name, vertex, minimum=0)
    if vertex >= matrix.shape[0]:
        raise ValueError(f"{name} must be smaller than the graph size")
    return vertex
