import numpy as np
import pytest

from data.input_generator import (
    generate_fractal_morphology,
    generate_botanical_graph,
    generate_random_control,
    generate_fibonacci_spiral,
    generate_voronoi_control,
    load_morphology,
)

GENERATORS = [
    generate_fractal_morphology,
    generate_botanical_graph,
    generate_random_control,
    generate_fibonacci_spiral,
    generate_voronoi_control,
]

MODES = ["fractal", "botanical", "random", "fibonacci", "voronoi"]


@pytest.mark.parametrize("generator", GENERATORS)
def test_shape_is_n_by_three(generator):
    nodes = generator(n_nodes=64, seed=42)
    assert nodes.shape == (64, 3)


@pytest.mark.parametrize("generator", GENERATORS)
def test_z_column_is_planar(generator):
    nodes = generator(n_nodes=64, seed=42)
    assert np.allclose(nodes[:, 2], 0.0)


@pytest.mark.parametrize("generator", GENERATORS)
def test_finite_coordinates(generator):
    nodes = generator(n_nodes=64, seed=42)
    assert np.all(np.isfinite(nodes))


@pytest.mark.parametrize("generator", GENERATORS)
def test_deterministic_with_seed(generator):
    first = generator(n_nodes=64, seed=42)
    second = generator(n_nodes=64, seed=42)
    assert np.array_equal(first, second)


@pytest.mark.parametrize("generator", GENERATORS)
def test_seed_changes_output(generator):
    first = generator(n_nodes=64, seed=42)
    other = generator(n_nodes=64, seed=7)
    assert not np.array_equal(first, other)


@pytest.mark.parametrize("generator", GENERATORS)
def test_custom_node_count(generator):
    nodes = generator(n_nodes=32, seed=42)
    assert nodes.shape == (32, 3)


@pytest.mark.parametrize("generator", GENERATORS)
def test_non_degenerate_spread(generator):
    nodes = generator(n_nodes=64, seed=42)
    spread = np.std(nodes[:, :2], axis=0)
    assert np.any(spread > 1e-6)


@pytest.mark.parametrize("mode", MODES)
def test_load_morphology_dispatch(mode):
    nodes = load_morphology(mode=mode, n_nodes=64, seed=42)
    assert nodes.shape == (64, 3)


def test_load_morphology_rejects_unknown_mode():
    with pytest.raises(ValueError):
        load_morphology(mode="nonexistent")


def test_voronoi_within_bounds():
    nodes = generate_voronoi_control(n_nodes=64, seed=42)
    assert nodes.shape == (64, 3)
    assert np.all(np.isfinite(nodes[:, :2]))
