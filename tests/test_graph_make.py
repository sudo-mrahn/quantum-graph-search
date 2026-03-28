import numpy as np
import pytest

from graph.attributes import check_symmetric
from graph.make import complete, cycle, erdos, erdos_nnconn, tree
from graph.process import count_edges, fill_to_total_edges


def test_complete_returns_symmetric_adjacency_matrix():
    adj = complete(5)

    assert adj.shape == (5, 5)
    assert np.all(np.diag(adj) == 0)
    assert check_symmetric(adj)


def test_tree_returns_expected_size():
    np.random.seed(0)
    adj = tree(6)

    assert adj.shape == (6, 6)
    assert np.count_nonzero(adj) == 10
    assert check_symmetric(adj)


def test_tree_size_one_returns_single_vertex():
    adj = tree(1)

    assert adj.shape == (1, 1)
    assert np.count_nonzero(adj) == 0


def test_erdos_nnconn_returns_partitioned_graph():
    np.random.seed(0)
    adj, communities = erdos_nnconn(12, 3, 0.5, 0.1)

    assert adj.shape == (12, 12)
    assert len(communities) == 3
    assert sum(len(comm) for comm in communities) == 12
    assert check_symmetric(adj)


def test_fill_to_total_edges_returns_new_graph_with_requested_edge_count():
    np.random.seed(0)
    adj = tree(5)

    filled = fill_to_total_edges(adj, total=6)

    assert count_edges(adj) == 4
    assert count_edges(filled) == 6
    assert check_symmetric(filled)


def test_cycle_rejects_too_many_spikes():
    with pytest.raises(ValueError):
        cycle(4, 2)


def test_erdos_rejects_invalid_subtype():
    with pytest.raises(ValueError):
        erdos(10, "z")
