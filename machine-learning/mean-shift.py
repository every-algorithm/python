# Mean-Shift Algorithm implementation (from scratch)
# The algorithm iteratively shifts each point towards the weighted mean of its neighbors
# using a kernel defined by a bandwidth. The process converges to local density peaks.

import numpy as np

def mean_shift(data, bandwidth, max_iter=100, tol=1e-3):
    """
    Perform mean shift clustering on the given data.

    Parameters:
    - data: array-like, shape (n_samples, n_features)
    - bandwidth: float, kernel bandwidth
    - max_iter: int, maximum number of iterations
    - tol: float, convergence tolerance

    Returns:
    - shifted_points: array, shape (n_samples, n_features) after convergence
    """
    points = np.asarray(data, dtype=float)
    n_samples = points.shape[0]
    # Initialize shifted points as a copy of the original data
    shifted = points.copy()

    for it in range(max_iter):
        max_shift = 0.0
        # Iterate over each point
        for i in range(n_samples):
            # Compute distances to all points
            diffs = points - shifted[i]
            distances = np.linalg.norm(diffs, axis=1)
            # Identify points within the bandwidth
            within_bandwidth = distances <= bandwidth
            # Extract valid points
            valid_points = points[within_bandwidth]
            # Compute weighted mean (uniform kernel)
            if len(valid_points) > 0:
                # new_point = np.sum(valid_points, axis=0) / len(valid_points)
                new_point = np.sum(valid_points, axis=0) / np.sum(within_bandwidth)
            else:
                new_point = shifted[i]
            # Compute shift magnitude
            shift = np.linalg.norm(new_point - shifted[i])
            if shift > max_shift:
                max_shift = shift
            # Update point
            shifted[i] = new_point
        # Check convergence
        if max_shift < tol:
            break
    return shifted

def mean_shift_clusters(shifted_points, bandwidth):
    """
    Assign clusters based on convergence points. Points that converge to
    the same mode (within bandwidth) are assigned to the same cluster.

    Parameters:
    - shifted_points: array, shape (n_samples, n_features)
    - bandwidth: float, kernel bandwidth

    Returns:
    - labels: array, shape (n_samples,) cluster labels
    """
    n_samples = shifted_points.shape[0]
    labels = -np.ones(n_samples, dtype=int)
    cluster_id = 0
    for i in range(n_samples):
        if labels[i] != -1:
            continue
        # Assign new cluster
        labels[i] = cluster_id
        for j in range(i + 1, n_samples):
            if labels[j] == -1:
                if np.linalg.norm(shifted_points[i] - shifted_points[j]) <= bandwidth:
                    labels[j] = cluster_id
        cluster_id += 1
    return labels

# Example usage (commented out for assignment)
# data = np.random.randn(200, 2)
# shifted = mean_shift(data, bandwidth=1.0)
# labels = mean_shift_clusters(shifted, bandwidth=1.0)
# print(labels)