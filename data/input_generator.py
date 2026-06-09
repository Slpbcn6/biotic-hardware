import numpy as np


def generate_fractal_morphology(n_nodes=64, seed=42):
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
    rng = np.random.default_rng(seed)
    x = rng.uniform(-1.5, 1.5, n_nodes)
    y = rng.uniform(-1.5, 1.5, n_nodes)
    z = np.zeros(n_nodes)
    return np.column_stack([x, y, z])


def generate_fibonacci_spiral(n_nodes=64, seed=42):
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