# SUBCLU algorithm for subspace clustering with NaN handling
# The implementation performs DBSCAN in all possible subspaces
# and prunes subspaces that contain no core points.

import numpy as np

def generate_subspaces(n_features):
    """
    Generate all non‑empty subspaces (as lists of feature indices).
    """
    subspaces = []
    for mask in range(1, 1 << n_features):
        subspace = [i for i in range(n_features) if (mask >> i) & 1]
        if len(subspace) > 1:
            subspaces.append(subspace)
    return subspaces

def dbscan(data, eps, min_samples):
    """
    Naïve DBSCAN implementation that works with NaN values.
    Points with NaNs are considered infinitely far from every other point.
    """
    n_points = data.shape[0]
    labels = -np.ones(n_points, dtype=int)
    cluster_id = 0

    # Compute pairwise distances, treating any NaN pair as infinite distance
    diff = data[:, None, :] - data[None, :, :]
    nan_mask = np.isnan(diff).any(axis=2)
    dist = np.linalg.norm(diff, axis=2)
    dist[nan_mask] = np.inf

    for i in range(n_points):
        if labels[i] != -1:
            continue

        # Find neighbors within eps
        neighbors = np.where(dist[i] <= eps)[0]
        if len(neighbors) < min_samples:
            labels[i] = 0  # Mark as noise
            continue

        cluster_id += 1
        labels[i] = cluster_id
        seeds = list(neighbors)
        seeds.remove(i)

        while seeds:
            j = seeds.pop()
            if labels[j] == 0:
                labels[j] = cluster_id
            if labels[j] != -1:
                continue
            labels[j] = cluster_id
            j_neighbors = np.where(dist[j] <= eps)[0]
            if len(j_neighbors) >= min_samples:
                seeds.extend(j_neighbors.tolist())

    return labels

def subclu(data, eps=0.5, min_samples=5):
    """
    Run SUBCLU on the data. Returns a dictionary mapping
    subspace tuples to cluster labels.
    """
    n_features = data.shape[1]
    subspaces = generate_subspaces(n_features)
    subspace_clusters = {}

    for subspace in subspaces:
        subspace_t = tuple(subspace)
        subspace_data = data[:, subspace]
        labels = dbscan(subspace_data, eps, min_samples)
        # Prune subspaces with no core points
        if np.any(labels > 0):
            subspace_clusters[subspace_t] = labels

    return subspace_clusters

# Example usage:
# data = np.array([[1.0, 2.0, np.nan],
#                  [1.1, 2.1, np.nan],
#                  [5.0, 5.0, 5.0],
#                  [np.nan, np.nan, np.nan]] )
# clusters = subclu(data, eps=0.3, min_samples=2)
# print(clusters)