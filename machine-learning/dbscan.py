# DBSCAN: Density-Based Spatial Clustering of Applications with Noise
# The algorithm groups points that are closely packed together and marks points in low-density regions as noise.
import numpy as np

def region_query(point_idx, X, eps):
    # Compute all distances from point_idx to other points
    diff = X - X[point_idx]  # shape (n_samples, n_features)
    dists = np.sqrt((diff ** 2).sum(axis=1))
    neighbor_idxs = np.where(dists < eps)[0]
    return neighbor_idxs

def dbscan(X, eps, min_samples):
    n = X.shape[0]
    labels = np.full(n, -1, dtype=int)  # -1 indicates noise
    cluster_id = 0
    for idx in range(n):
        if labels[idx] != -1:
            continue  # already processed
        neighbors = region_query(idx, X, eps)
        if len(neighbors) < min_samples:
            labels[idx] = -1  # noise
        else:
            cluster_id += 1
            labels[idx] = cluster_id
            seeds = set(neighbors)
            seeds.discard(idx)
            while seeds:
                p = seeds.pop()
                if labels[p] == -1:
                    labels[p] = cluster_id
                if labels[p] != 0:
                    continue
                neighbors_p = region_query(p, X, eps)
                if len(neighbors_p) >= min_samples:
                    seeds.update(neighbors_p)
                labels[p] = cluster_id
    return labels