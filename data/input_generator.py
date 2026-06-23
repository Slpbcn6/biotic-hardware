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


def generate_hexagonal_lattice(n_nodes=64, seed=42):
    """Generate a hexagonal (triangular) lattice morphology.

    Nodes occupy a row-offset triangular lattice with spacing 0.4, centred on
    the origin, with a small Gaussian jitter (std 0.03). Like the fractal and
    Fibonacci morphologies, the layout is geometrically deterministic and
    effectively seed-frozen: the jitter is cosmetic and carries no real
    between-seed variance.

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
    spacing = 0.4
    cols = int(np.ceil(np.sqrt(n_nodes))) + 1
    rows = int(np.ceil(n_nodes / cols)) + 2
    dy = spacing * np.sqrt(3.0) / 2.0
    coords = []
    for r in range(rows):
        for c in range(cols):
            x = c * spacing + (r % 2) * spacing / 2.0
            y = r * dy
            coords.append([x, y])
    coords = np.array(coords[:n_nodes], dtype=float)
    coords -= coords.mean(axis=0)
    coords = coords + rng.normal(0, 0.03, coords.shape)
    z = np.zeros((len(coords), 1))
    return np.column_stack([coords, z])


def generate_dla_aggregate(n_nodes=64, seed=42):
    """Generate a diffusion-limited aggregation (DLA) morphology.

    Starting from a single seed particle at the origin, particles are released
    from a spawn circle and perform a random walk until they touch the growing
    cluster, where they stick. The mechanism produces dendritic, tip-biased
    growth that is genuinely stochastic, so different seeds yield different
    aggregates (real between-seed variance). Each particle sticks within the
    contact distance of an existing node, so the point set is connected.

    Parameters
    ----------
    n_nodes : int
        Number of nodes to generate.
    seed : int
        Seed for the random-walk RNG.

    Returns
    -------
    ndarray, shape (n_nodes, 3)
        Node coordinates; the z column is zero (planar).
    """
    rng = np.random.default_rng(seed)
    contact = 0.35
    step = 0.35
    nodes = [np.array([0.0, 0.0])]
    while len(nodes) < n_nodes:
        cluster = np.array(nodes)
        cluster_radius = float(np.max(np.linalg.norm(cluster, axis=1)))
        spawn_radius = cluster_radius + 2.0
        kill_radius = spawn_radius + 6.0
        ang = rng.uniform(0, 2 * np.pi)
        pos = np.array([np.cos(ang), np.sin(ang)]) * spawn_radius
        for _ in range(6000):
            d = float(np.min(np.linalg.norm(cluster - pos, axis=1)))
            if d <= contact:
                break
            theta = rng.uniform(0, 2 * np.pi)
            pos = pos + step * np.array([np.cos(theta), np.sin(theta)])
            if np.linalg.norm(pos) > kill_radius:
                ang = rng.uniform(0, 2 * np.pi)
                pos = np.array([np.cos(ang), np.sin(ang)]) * spawn_radius
        nodes.append(pos)
    pts = np.array(nodes)
    pts -= pts.mean(axis=0)
    z = np.zeros((len(pts), 1))
    return np.column_stack([pts, z])


def generate_clustered_morphology(n_nodes=64, seed=42):
    """Generate a modular clustered morphology of dense blobs.

    Four Gaussian blobs are placed around the origin at a base radius with
    seeded angular and radial perturbation, and members are scattered around
    each blob centre. The arrangement is compact enough that the blobs remain
    mutually connected, while the dense intra-blob structure gives a high
    clustering coefficient. The layout is genuinely stochastic (real
    between-seed variance).

    Parameters
    ----------
    n_nodes : int
        Number of nodes to generate.
    seed : int
        Seed for the cluster-placement RNG.

    Returns
    -------
    ndarray, shape (n_nodes, 3)
        Node coordinates; the z column is zero (planar).
    """
    rng = np.random.default_rng(seed)
    n_clusters = 4
    base_angles = np.linspace(0, 2 * np.pi, n_clusters, endpoint=False)
    rotation = rng.uniform(0, 2 * np.pi)
    centres = []
    for a in base_angles:
        ang = a + rotation + rng.normal(0, 0.15)
        radius = 0.9 + rng.normal(0, 0.1)
        centres.append([radius * np.cos(ang), radius * np.sin(ang)])
    centres = np.array(centres)
    base = n_nodes // n_clusters
    counts = [base] * n_clusters
    for i in range(n_nodes - base * n_clusters):
        counts[i] += 1
    blocks = []
    for centre, count in zip(centres, counts):
        members = centre + rng.normal(0, 0.28, (count, 2))
        blocks.append(members)
    pts = np.vstack(blocks)
    z = np.zeros((len(pts), 1))
    return np.column_stack([pts, z])


def generate_concentric_rings(n_nodes=64, seed=42):
    """Generate a concentric-ring morphology.

    Nodes are distributed across four concentric rings of radius 0.5, 1.0, 1.5
    and 2.0, with the node budget allocated in proportion to ring radius. Each
    ring is independently rotated by a seeded angle and perturbed with angular
    and radial jitter, so the relative configuration between rings changes from
    seed to seed (real between-seed variance). Adjacent rings are half a unit
    apart, keeping the point set connected.

    Parameters
    ----------
    n_nodes : int
        Number of nodes to generate.
    seed : int
        Seed for the per-ring rotation and jitter RNG.

    Returns
    -------
    ndarray, shape (n_nodes, 3)
        Node coordinates; the z column is zero (planar).
    """
    rng = np.random.default_rng(seed)
    radii = np.array([0.5, 1.0, 1.5, 2.0])
    counts = np.floor(radii / radii.sum() * n_nodes).astype(int)
    counts[-1] += n_nodes - int(counts.sum())
    blocks = []
    for radius, count in zip(radii, counts):
        if count <= 0:
            continue
        rotation = rng.uniform(0, 2 * np.pi)
        base = np.linspace(0, 2 * np.pi, count, endpoint=False) + rotation
        angles = base + rng.normal(0, 0.12, count)
        radial = radius + rng.normal(0, 0.08, count)
        x = radial * np.cos(angles)
        y = radial * np.sin(angles)
        blocks.append(np.column_stack([x, y]))
    pts = np.vstack(blocks)
    z = np.zeros((len(pts), 1))
    return np.column_stack([pts, z])


def generate_reticulate_mesh(n_nodes=64, seed=42):
    """Generate a reticulate (vein-like) morphology by branching filament growth.

    Filaments grow as random walks of fixed step length that branch with a
    small probability, producing an anisotropic net of veins rather than a
    uniform mesh. Each node is placed within one step of its parent, so the
    point set is connected by construction, and growth is confined to a bounded
    region by steering tips back towards the centre when they drift too far, so
    separate veins cross and form loops. Random directions and branch points
    give genuine between-seed variance, and the locally one-dimensional vein
    structure occupies a distinct region of the topology space from the regular
    and clustered morphologies.

    Parameters
    ----------
    n_nodes : int
        Number of nodes to generate.
    seed : int
        Seed for the growth RNG.

    Returns
    -------
    ndarray, shape (n_nodes, 3)
        Node coordinates; the z column is zero (planar).
    """
    rng = np.random.default_rng(seed)
    step = 0.45
    branch_prob = 0.35
    radius_limit = 2.6
    points = [np.array([0.0, 0.0])]
    tips = [{"pos": np.array([0.0, 0.0]), "angle": rng.uniform(0.0, 2.0 * np.pi)}]
    n_seed_tips = 3
    for _ in range(n_seed_tips):
        tips.append({"pos": np.array([0.0, 0.0]), "angle": rng.uniform(0.0, 2.0 * np.pi)})
    while len(points) < n_nodes and tips:
        idx = rng.integers(0, len(tips))
        tip = tips[idx]
        angle = tip["angle"] + rng.normal(0.0, 0.4)
        pos = tip["pos"]
        if np.linalg.norm(pos) > radius_limit:
            home = np.arctan2(-pos[1], -pos[0])
            angle = home + rng.normal(0.0, 0.5)
        new_pos = pos + step * np.array([np.cos(angle), np.sin(angle)])
        points.append(new_pos)
        tip["pos"] = new_pos
        tip["angle"] = angle
        if rng.random() < branch_prob and len(tips) < n_nodes:
            tips.append({"pos": new_pos.copy(), "angle": angle + rng.uniform(0.6, 1.2)})
    pts = np.array(points[:n_nodes], dtype=float)
    pts = pts - pts.mean(axis=0)
    pts = pts + rng.normal(0, 0.02, pts.shape)
    z = np.zeros((len(pts), 1))
    return np.column_stack([pts, z])


def load_morphology(mode="fractal", n_nodes=64, seed=42):
    """Dispatch to a morphology generator by name.

    Parameters
    ----------
    mode : str
        One of: 'fractal', 'botanical', 'random', 'fibonacci', 'voronoi',
        'hexagonal', 'dla', 'clusters', 'concentric', 'reticulate'.
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
        "fractal":     generate_fractal_morphology,
        "botanical":   generate_botanical_graph,
        "random":      generate_random_control,
        "fibonacci":   generate_fibonacci_spiral,
        "voronoi":     generate_voronoi_control,
        "hexagonal":   generate_hexagonal_lattice,
        "dla":         generate_dla_aggregate,
        "clusters":    generate_clustered_morphology,
        "concentric":  generate_concentric_rings,
        "reticulate":  generate_reticulate_mesh,
    }
    if mode not in generators:
        raise ValueError(f"Unknown morphology mode: {mode}")
    return generators[mode](n_nodes=n_nodes, seed=seed)