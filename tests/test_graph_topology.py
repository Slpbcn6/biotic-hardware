import numpy as np
import pytest

from data.graph_topology import (
    build_knn_graph,
    laplacian,
    spectral_metrics,
    clustering_coefficient,
    degree_stats,
    path_metrics,
    compute_topology,
)


def cycle_adjacency(n):
    a = np.zeros((n, n))
    for i in range(n):
        a[i, (i + 1) % n] = 1.0
        a[i, (i - 1) % n] = 1.0
    return a


def complete_adjacency(n):
    a = np.ones((n, n))
    np.fill_diagonal(a, 0.0)
    return a


def two_disconnected_complete(n):
    block = complete_adjacency(n)
    a = np.zeros((2 * n, 2 * n))
    a[:n, :n] = block
    a[n:, n:] = block
    return a


def test_complete_graph_spectrum():
    n = 8
    sm = spectral_metrics(complete_adjacency(n))
    assert sm["n_components"] == 1
    assert np.isclose(sm["lambda_2"], n)
    assert np.isclose(sm["lambda_max"], n)
    assert np.isclose(sm["eigenratio"], 1.0)


def test_complete_graph_clustering_is_one():
    assert np.isclose(clustering_coefficient(complete_adjacency(6)), 1.0)


def test_cycle_graph_spectrum():
    n = 6
    sm = spectral_metrics(cycle_adjacency(n))
    assert sm["n_components"] == 1
    assert np.isclose(sm["lambda_2"], 2 - 2 * np.cos(2 * np.pi / n))
    assert np.isclose(sm["lambda_max"], 4.0)


def test_cycle_graph_clustering_is_zero():
    assert np.isclose(clustering_coefficient(cycle_adjacency(8)), 0.0)


def test_disconnected_graph_reports_nan():
    sm = spectral_metrics(two_disconnected_complete(3))
    assert sm["n_components"] == 2
    assert np.isnan(sm["lambda_2"])
    assert np.isnan(sm["eigenratio"])


def test_laplacian_rows_sum_to_zero():
    a = cycle_adjacency(7)
    rows = laplacian(a).sum(axis=1)
    assert np.allclose(rows, 0.0)


def test_degree_stats_complete_graph():
    n = 5
    stats = degree_stats(complete_adjacency(n))
    assert stats["n_nodes"] == n
    assert stats["n_edges"] == n * (n - 1) // 2
    assert np.isclose(stats["mean_degree"], n - 1)
    assert np.isclose(stats["density"], 1.0)


def test_path_metrics_cycle_diameter():
    n = 8
    pm = path_metrics(cycle_adjacency(n))
    assert pm["diameter"] == n // 2


def test_path_metrics_disconnected_is_nan():
    pm = path_metrics(two_disconnected_complete(4))
    assert np.isnan(pm["char_path_length"])
    assert np.isnan(pm["diameter"])


def test_knn_graph_is_symmetric_without_self_loops():
    rng = np.random.default_rng(0)
    pts = rng.uniform(-1, 1, (20, 2))
    a = build_knn_graph(pts, k=4)
    assert np.array_equal(a, a.T)
    assert np.allclose(np.diag(a), 0.0)


def test_knn_graph_min_degree_at_least_k():
    rng = np.random.default_rng(1)
    pts = rng.uniform(-1, 1, (30, 2))
    k = 5
    a = build_knn_graph(pts, k=k)
    degree = a.sum(axis=1)
    assert np.all(degree >= k)


def test_knn_graph_caps_k_at_n_minus_one():
    pts = np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]])
    a = build_knn_graph(pts, k=10)
    assert np.array_equal(a, complete_adjacency(3))


def test_compute_topology_on_point_set():
    rng = np.random.default_rng(2)
    pts = rng.uniform(-1.5, 1.5, (40, 3))
    record = compute_topology(pts, k=6)
    assert record["k"] == 6
    assert record["n_nodes"] == 40
    assert record["mean_degree"] >= 6
    assert 0.0 <= record["clustering_coefficient"] <= 1.0


@pytest.mark.parametrize("n", [5, 7, 10])
def test_complete_graph_eigenratio_is_one(n):
    sm = spectral_metrics(complete_adjacency(n))
    assert np.isclose(sm["eigenratio"], 1.0)
