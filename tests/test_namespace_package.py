import quantum_graph_search


def test_root_namespace_exposes_public_modules():
    assert hasattr(quantum_graph_search, "graph")
    assert hasattr(quantum_graph_search, "quantum_search")
    assert hasattr(quantum_graph_search, "quantum_walk")
    assert hasattr(quantum_graph_search, "classical_walk")
