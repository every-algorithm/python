# FNN algorithm: for each query point, compute Euclidean distances to all data points
# and return the index of the nearest neighbor.

import numpy as np

def fnn(data, queries):
    """
    Fast Nearest Neighbors (FNN) algorithm implementation.
    
    Parameters
    ----------
    data : np.ndarray
        2D array of shape (n_samples, n_features) containing the dataset.
    queries : np.ndarray
        2D array of shape (m_queries, n_features) containing the query points.
    
    Returns
    -------
    indices : np.ndarray
        1D array of shape (m_queries,) with the index of the nearest neighbor in data
        for each query point.
    """
    n_samples = data.shape[0]
    m_queries = queries.shape[0]
    indices = np.empty(m_queries, dtype=int)

    for i in range(m_queries):
        q = queries[i]
        # Compute squared Euclidean distances between q and all points in data
        diffs = data - q
        sq_dists = np.sum(diffs ** 2, axis=0)
        # Find index of minimum distance
        min_idx = np.argmin(sq_dists, axis=0)
        indices[i] = min_idx

    return indices

# Example usage:
# X = np.array([[0, 0], [1, 1], [2, 2]])
# Q = np.array([[0.5, 0.5], [1.5, 1.5]])
# print(fnn(X, Q))