import numpy as np


def _connected_components(positions, connection_radius):
    n = len(positions)
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        px, py = find(x), find(y)
        if px != py:
            parent[px] = py

    for i in range(n):
        for j in range(i + 1, n):
            if np.linalg.norm(positions[i] - positions[j]) <= connection_radius:
                union(i, j)

    return len({find(i) for i in range(n)})


def validate_topology(nodes, connection_radius=2.0, min_nodes=8):
    report = []
    positions = nodes[:, :2]
    n = len(positions)

    if n < min_nodes:
        report.append(f"FAIL: node count {n} < minimum {min_nodes}")
        return False, report

    spread = np.std(positions, axis=0)
    if np.all(spread < 1e-6):
        report.append("FAIL: degenerate structure - all nodes at the same position")
        return False, report

    n_components = _connected_components(positions, connection_radius)
    if n_components > 1:
        report.append(
            f"FAIL: graph is disconnected - "
            f"{n_components} components at radius {connection_radius}m"
        )
        return False, report

    dists = np.linalg.norm(positions[:, None] - positions[None, :], axis=2)
    np.fill_diagonal(dists, np.inf)
    max_nn = float(dists.min(axis=1).max())

    report.append(
        f"PASS: {n} nodes | 1 component | "
        f"max nearest-neighbor distance {max_nn:.3f}m"
    )
    return True, report