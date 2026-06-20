import numpy as np
import pytest

from data.topology_validator import validate_topology, _connected_components


def _grid(spacing=0.5, side=4):
    nodes = []
    for i in range(side):
        for j in range(side):
            nodes.append([i * spacing, j * spacing, 0.0])
    return np.array(nodes)


def test_connected_grid_passes():
    nodes = _grid(spacing=0.5, side=4)
    ok, report = validate_topology(nodes, connection_radius=0.6, min_nodes=8)
    assert ok
    assert any("PASS" in line for line in report)


def test_too_few_nodes_fails():
    nodes = _grid(spacing=0.5, side=2)
    ok, report = validate_topology(nodes, connection_radius=2.0, min_nodes=8)
    assert not ok
    assert any("node count" in line for line in report)


def test_degenerate_structure_fails():
    nodes = np.zeros((16, 3))
    ok, report = validate_topology(nodes, connection_radius=2.0, min_nodes=8)
    assert not ok
    assert any("degenerate" in line for line in report)


def test_disconnected_graph_fails():
    cluster_a = _grid(spacing=0.3, side=3)
    cluster_b = _grid(spacing=0.3, side=3) + np.array([100.0, 100.0, 0.0])
    nodes = np.vstack([cluster_a, cluster_b])
    ok, report = validate_topology(nodes, connection_radius=0.4, min_nodes=8)
    assert not ok
    assert any("disconnected" in line for line in report)


def test_connected_components_single():
    nodes = _grid(spacing=0.5, side=4)
    assert _connected_components(nodes[:, :2], 0.6) == 1


def test_connected_components_two():
    cluster_a = _grid(spacing=0.3, side=3)[:, :2]
    cluster_b = cluster_a + np.array([50.0, 50.0])
    positions = np.vstack([cluster_a, cluster_b])
    assert _connected_components(positions, 0.4) == 2


@pytest.mark.parametrize("mode", [
    "fractal", "botanical", "random", "fibonacci", "voronoi",
    "hexagonal", "dla", "clusters", "concentric", "reticulate",
])
def test_generated_morphologies_validate(mode):
    from data.input_generator import load_morphology
    nodes = load_morphology(mode=mode, n_nodes=64, seed=42)
    ok, report = validate_topology(nodes, connection_radius=2.0, min_nodes=8)
    assert ok, report
    assert len(report) >= 1
