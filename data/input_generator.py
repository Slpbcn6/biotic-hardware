import numpy as np


def generate_fractal_morphology(n_nodes=64, seed=42):
    """Generate a deterministic fractal morphology as a planar point set.

    Nodes are placed along a self-similar rose curve r = 1 + 0.4 sin(3t)
    swept over [0, 8π], with a small Gaussian jitter (std 0.03). Because the
    layout is geometrically deterministic, the point set is effectively
    seed-frozen: the jitter is cosmetic and carries no real between-seed
    variance.

    Parameters
    ----------
    n_nodes : int
        Number of nodes to generate.
    seed : int
        Seed for the jitter RNG.

    Returns
    -------
    ndarray, shape (n_nodes, 3)
        Node coordinates; the z column is zero (planar).
    """
    rng = np.random.default_rng(seed)
    nodes = []
    for i in range(n_nodes):
        t = i / n_nodes * 8 * np.pi
        r = 1.0 + 0.4 * np.sin(3 * t)
        x = r * np.cos(t) + rng.normal(0, 0.03)
        y = r * np.sin(t) + rng.normal(0, 0.03)
        nodes.append([x, y, 0.0])
    return np.array(nodes)


def generate_botanical_graph(n_nodes=64, seed=42):
    """Generate a stochastic botanical morphology by random branching.

    Starting from a root at the origin, each new node attaches to a randomly
    chosen existing node at a seeded angle and radius, producing a branched
    tree. The structure is genuinely stochastic, so different seeds yield
    different graphs (real between-seed variance).

    Parameters
    ----------
    n_nodes : int
        Number of nodes to generate.
    seed : int
        Seed for the branching RNG.

    Returns
    -------
    ndarray, shape (n_nodes, 3)
        Node coordinates; the z column is zero (planar).
    """
    rng = np.random.default_rng(seed)
    nodes = [[0.0, 0.0, 0.0]]
    angles = np.linspace(0, 2 * np.pi, n_nodes, endpoint=False)
    for i in range(1, n_nodes):
        parent = rng.integers(0, len(nodes))
        base = np.array(nodes[parent])
        angle = angles[i] + rng.normal(0, 0.2)
        radius = 0.2 + 0.8 * rng.random()
        new_node = base + np.array([
            np.cos(angle) * radius,
            np.sin(angle) * radius,
            0.0,
        ])
        nodes.append(new_node)
    return np.array(nodes)


def generate_random_control(n_nodes=64, seed=42):
    """Generate an unstructured random control morphology.

    Nodes are drawn uniformly in the square [-1.5, 1.5]^2. This is the
    baseline against which structured morphologies are compared.

    Parameters
    ----------
    n_nodes : int
        Number of nodes to generate.
    seed : int
        Seed for the uniform RNG.

    Returns
    -------
    ndarray, shape (n_nodes, 3)
        Node coordinates; the z column is zero (planar).
    """
    rng = np.random.default_rng(seed)
    x = rng.uniform(-1.5, 1.5, n_nodes)
    y = rng.uniform(-1.5, 1.5, n_nodes)
    z = np.zeros(n_nodes)
    return np.column_stack([x, y, z])


def generate_fibonacci_spiral(n_nodes=64, seed=42):
    """Generate a Fibonacci spiral morphology using the golden angle.

    Nodes follow a sunflower-style phyllotaxis spiral with golden angle
    π(3 − √5) ≈ 137.508°, with a small Gaussian jitter (std 0.03). Like the
    fractal morphology, the layout is geometrically deterministic and
    effectively seed-frozen.

    Parameters
    ----------
    n_nodes : int
        Number of nodes to generate.
    seed : int
        Seed for the jitter RNG.

    Returns
    -------
    ndarray, shape (n_nodes, 3)
        Node coordinates; the z column is zero (planar).
    """
    rng = np.random.default_rng(seed)
    golden_angle = np.pi * (3.0 - np.sqrt(5.0))
    nodes = []
    for i in range(n_nodes):
        r = np.sqrt(i / n_nodes) * 2.0
        theta = i * golden_angle
        x = r * np.cos(theta) + rng.normal(0, 0.03)
        y = r * np.sin(theta) + rng.normal(0, 0.03)
        nodes.append([x, y, 0.0])
    return np.array(nodes)


def generate_voronoi_control(n_nodes=64, seed=42):
    """Generate a Voronoi control morphology from a uniform random seed set.

    A set of 4*n_nodes uniform seeds is triangulated, and the finite Voronoi
    vertices falling within the domain bounds (|coord| <= 2.0) are used as
    nodes. When fewer than n_nodes qualify, the remainder is filled with
    uniform random points in [-1.5, 1.5], keeping the control a fixed-size,
    reproducible point set. This is a stochastic control with real
    between-seed variance.

    Parameters
    ----------
    n_nodes : int
        Number of nodes to generate.
    seed : int
        Seed for the Voronoi seed set and the fallback fill.

    Returns
    -------
    ndarray, shape (n_nodes, 3)
        Node coordinates; the z column is zero (planar).
    """
    from scipy.spatial import Voronoi
    rng = np.random.default_rng(seed)
    seeds = rng.uniform(-2.0, 2.0, (n_nodes * 4, 2))
    vor = Voronoi(seeds)
    verts = vor.vertices
    mask = np.all(np.abs(verts) <= 2.0, axis=1)
    finite = verts[mask]
    if len(finite) >= n_nodes:
        idx = rng.choice(len(finite), size=n_nodes, replace=False)
        chosen = finite[idx]
    else:
        extra_n = n_nodes - len(finite)
        extra = rng.uniform(-1.5, 1.5, (extra_n, 2))
        chosen = np.vstack([finite, extra])
    z = np.zeros((n_nodes, 1))
    return np.column_stack([chosen, z])


def load_morphology(mode="fractal", n_nodes=64, seed=42):
    """Dispatch to a morphology generator by name.

    Parameters
    ----------
    mode : str
        One of: 'fractal', 'botanical', 'random', 'fibonacci', 'voronoi'.
    n_nodes : int
        Number of nodes to generate.
    seed : int
        Seed forwarded to the selected generator.

    Returns
    -------
    ndarray, shape (n_nodes, 3)
        Node coordinates from the selected generator.

    Raises
    ------
    ValueError
        If mode is not a known morphology.
    """
    generators = {
        "fractal":   generate_fractal_morphology,
        "botanical": generate_botanical_graph,
        "random":    generate_random_control,
        "fibonacci": generate_fibonacci_spiral,
        "voronoi":   generate_voronoi_control,
    }
    if mode not in generators:
        raise ValueError(f"Unknown morphology mode: {mode}")
    return generators[mode](n_nodes=n_nodes, seed=seed)