import quantum_graph_search
from quantum_graph_search import classical_walk, graph, quantum_search, quantum_walk


def test_root_namespace_exposes_public_modules():
    assert hasattr(quantum_graph_search, "graph")
    assert hasattr(quantum_graph_search, "quantum_search")
    assert hasattr(quantum_graph_search, "quantum_walk")
    assert hasattr(quantum_graph_search, "classical_walk")


def test_public_modules_expose_supported_entrypoints():
    assert hasattr(graph, "complete")
    assert hasattr(quantum_search, "simulate")
    assert hasattr(quantum_walk, "get_mean_distance_series")
    assert hasattr(classical_walk, "walk")


def test_public_modules_do_not_expose_research_only_submodules():
    assert not hasattr(quantum_search, "notunitary")
    assert not hasattr(quantum_search, "process")
    assert not hasattr(quantum_search, "unitary")
    assert not hasattr(quantum_walk, "lintrans")
    assert not hasattr(quantum_walk, "notunitary")
    assert not hasattr(quantum_walk, "unitary")
