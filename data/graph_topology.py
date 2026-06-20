import numpy as np
from scipy.linalg import eigh
from scipy.sparse.csgraph import shortest_path, connected_components

_ZERO_TOL = 1e-9


def build_knn_graph(positions, k):
    """Build an undirected k-nearest-neighbour graph from a planar point set.

    Each node is linked to its k nearest neighbours by Euclidean distance in
    the x, y plane. The directed k-NN relation is symmetrised by union: an
    undirected edge i--j exists when j is among the k nearest of i OR i is
    among the k nearest of j. The union convention guarantees every node has
    degree at least k and keeps the graph undirected, which is required for the
    real-symmetric Laplacian spectrum used downstream.

    Parameters
    ----------
    positions : ndarray, shape (n, 2) or (n, 3)
        Node coordinates; only the first two columns (x, y) are used.
    k : int
        Number of nearest neighbours per node. Capped at n - 1.

    Returns
    -------
    ndarray, shape (n, n)
        Symmetric binary adjacency matrix with a zero diagonal.
    """
    pts = np.asarray(positions, dtype=float)[:, :2]
    n = len(pts)
    if n < 2:
        return np.zeros((n, n), dtype=float)
    k_eff = int(min(k, n - 1))
    diff = pts[:, None, :] - pts[None, :, :]
    dists = np.sqrt(np.sum(diff * diff, axis=2))
    np.fill_diagonal(dists, np.inf)
    adjacency = np.zeros((n, n), dtype=float)
    nearest = np.argsort(dists, axis=1)[:, :k_eff]
    for i in range(n):
        adjacency[i, nearest[i]] = 1.0
    adjacency = np.maximum(adjacency, adjacency.T)
    np.fill_diagonal(adjacency, 0.0)
    return adjacency


def laplacian(adjacency):
    """Return the combinatorial graph Laplacian L = D - A.

    Parameters
    ----------
    adjacency : ndarray, shape (n, n)
        Symmetric adjacency matrix.

    Returns
    -------
    ndarray, shape (n, n)
        The Laplacian matrix.
    """
    a = np.asarray(adjacency, dtype=float)
    degree = np.diag(a.sum(axis=1))
    return degree - a


def spectral_metrics(adjacency):
    """Compute Laplacian spectral descriptors of synchronisability.

    Diagonalises the symmetric Laplacian L = D - A and reads off the algebraic
    connectivity (second-smallest eigenvalue lambda_2), the largest eigenvalue
    lambda_max, and the eigenratio R = lambda_max / lambda_2. In the master
    stability framework (Barahona & Pecora 2002) a smaller R indicates a wider
    window of stable synchronisation. The number of (near-)zero eigenvalues
    equals the number of connected components; when the graph is disconnected
    lambda_2 is zero and R diverges, so both are reported as NaN rather than a
    silent zero or infinity.

    Parameters
    ----------
    adjacency : ndarray, shape (n, n)
        Symmetric adjacency matrix.

    Returns
    -------
    dict
        Keys: 'n_components', 'lambda_2', 'lambda_max', 'eigenratio'.
        'lambda_2' and 'eigenratio' are NaN when the graph is disconnected.
    """
    a = np.asarray(adjacency, dtype=float)
    n = a.shape[0]
    if n < 2:
        return {
            "n_components": n,
            "lambda_2": float("nan"),
            "lambda_max": 0.0,
            "eigenratio": float("nan"),
        }
    eigvals = eigh(laplacian(a), eigvals_only=True)
    eigvals = np.clip(np.sort(eigvals), 0.0, None)
    n_components = int(np.sum(eigvals < _ZERO_TOL))
    n_components = max(n_components, 1)
    lambda_max = float(eigvals[-1])
    if n_components > 1:
        return {
            "n_components": n_components,
            "lambda_2": float("nan"),
            "lambda_max": lambda_max,
            "eigenratio": float("nan"),
        }
    lambda_2 = float(eigvals[1])
    eigenratio = float(lambda_max / lambda_2) if lambda_2 > _ZERO_TOL else float("nan")
    return {
        "n_components": 1,
        "lambda_2": lambda_2,
        "lambda_max": lambda_max,
        "eigenratio": eigenratio,
    }


def clustering_coefficient(adjacency):
    """Compute the average local clustering coefficient (Watts-Strogatz).

    For each node the local coefficient is the fraction of realised edges among
    its neighbours relative to the maximum possible; nodes of degree below two
    contribute zero. The returned value is the unweighted mean across all
    nodes. It is 1.0 for a complete graph and 0.0 for a simple cycle.

    Parameters
    ----------
    adjacency : ndarray, shape (n, n)
        Symmetric adjacency matrix.

    Returns
    -------
    float
        Mean local clustering coefficient in [0, 1].
    """
    a = (np.asarray(adjacency, dtype=float) > 0).astype(float)
    np.fill_diagonal(a, 0.0)
    n = a.shape[0]
    degree = a.sum(axis=1)
    coeffs = np.zeros(n)
    for i in range(n):
        if degree[i] < 2:
            continue
        neighbours = np.where(a[i] > 0)[0]
        sub = a[np.ix_(neighbours, neighbours)]
        realised = sub.sum() / 2.0
        possible = degree[i] * (degree[i] - 1) / 2.0
        coeffs[i] = realised / possible
    return float(np.mean(coeffs))


def degree_stats(adjacency):
    """Summarise basic degree and density statistics of a graph.

    Parameters
    ----------
    adjacency : ndarray, shape (n, n)
        Symmetric adjacency matrix.

    Returns
    -------
    dict
        Keys: 'n_nodes', 'n_edges', 'mean_degree', 'density'.
    """
    a = (np.asarray(adjacency, dtype=float) > 0).astype(float)
    np.fill_diagonal(a, 0.0)
    n = a.shape[0]
    degree = a.sum(axis=1)
    n_edges = int(a.sum() / 2)
    mean_degree = float(degree.mean()) if n > 0 else 0.0
    density = float(2 * n_edges / (n * (n - 1))) if n > 1 else 0.0
    return {
        "n_nodes": n,
        "n_edges": n_edges,
        "mean_degree": mean_degree,
        "density": density,
    }


def path_metrics(adjacency):
    """Compute characteristic path length and diameter of a graph.

    Shortest paths are computed on the unweighted, undirected graph. When the
    graph has more than one connected component both metrics are reported as
    NaN, since path length between components is undefined.

    Parameters
    ----------
    adjacency : ndarray, shape (n, n)
        Symmetric adjacency matrix.

    Returns
    -------
    dict
        Keys: 'char_path_length', 'diameter'.
    """
    a = (np.asarray(adjacency, dtype=float) > 0).astype(float)
    n = a.shape[0]
    if n < 2:
        return {"char_path_length": float("nan"), "diameter": float("nan")}
    n_comp, _ = connected_components(a, directed=False)
    if n_comp > 1:
        return {"char_path_length": float("nan"), "diameter": float("nan")}
    dmat = shortest_path(a, method="D", directed=False, unweighted=True)
    iu = np.triu_indices_from(dmat, k=1)
    vals = dmat[iu]
    return {
        "char_path_length": float(np.mean(vals)),
        "diameter": float(np.max(vals)),
    }


def compute_topology(positions, k):
    """Build a k-NN graph from a point set and compute all topology metrics.

    Combines degree statistics, Laplacian spectral descriptors, the clustering
    coefficient and path metrics into a single record. This is the per-graph
    entry point used by the topology analysis step.

    Parameters
    ----------
    positions : ndarray, shape (n, 2) or (n, 3)
        Node coordinates; only x, y are used.
    k : int
        Number of nearest neighbours used to build the graph.

    Returns
    -------
    dict
        Merged metrics record, including the resolved 'k'.
    """
    adjacency = build_knn_graph(positions, k)
    record = {"k": int(k)}
    record.update(degree_stats(adjacency))
    record.update(spectral_metrics(adjacency))
    record["clustering_coefficient"] = clustering_coefficient(adjacency)
    record.update(path_metrics(adjacency))
    return record
