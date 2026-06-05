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
            0.0
        ])

        nodes.append(new_node)

    return np.array(nodes)


def generate_random_control(n_nodes=64, seed=42):
    """
    Baseline control morphology: uniformly random node positions.
    Spatial range matches fractal/botanical extent (~[-2, 2]).
    Same n_nodes and seed as bio-inspired morphologies for fair comparison.
    """
    rng = np.random.default_rng(seed)

    x = rng.uniform(-1.5, 1.5, n_nodes)
    y = rng.uniform(-1.5, 1.5, n_nodes)
    z = np.zeros(n_nodes)

    return np.column_stack([x, y, z])


def load_morphology(mode="fractal"):
    if mode == "fractal":
        return generate_fractal_morphology()
    elif mode == "botanical":
        return generate_botanical_graph()
    elif mode == "random":
        return generate_random_control()
    else:
        raise ValueError("Unknown morphology mode")