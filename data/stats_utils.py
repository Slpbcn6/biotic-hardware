import numpy as np

def cohens_d(a, b):
    a, b = np.array(a, dtype=float), np.array(b, dtype=float)
    pooled = np.sqrt((np.std(a, ddof=1) ** 2 + np.std(b, ddof=1) ** 2) / 2)
    if pooled < 1e-4:
        return float("nan")
    return float((np.mean(a) - np.mean(b)) / pooled)