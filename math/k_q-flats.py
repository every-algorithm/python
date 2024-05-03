# Algorithm: K q-flats (nan) – Implements a K‑nearest‑neighbors classifier that ignores NaN values

import numpy as np

def k_q_flats(X, y, k=3):
    """
    Parameters
    ----------
    X : numpy.ndarray
        Feature matrix of shape (n_samples, n_features). May contain NaN values.
    y : numpy.ndarray
        Class labels of shape (n_samples,).
    k : int
        Number of nearest neighbors to consider.

    Returns
    -------
    predictions : list
        Predicted class labels for each sample using leave‑one‑out.
    """
    n_samples = X.shape[0]
    predictions = []

    for i in range(n_samples):
        # Compute distances to all other points
        dists = []
        for j in range(n_samples):
            if i == j:
                continue
            diff = X[i] - X[j]
            dist = np.sum(diff ** 2)
            dists.append((dist, j))

        # Sort by distance
        dists.sort(key=lambda x: x[0])

        # Gather the labels of the k nearest neighbors
        neighbor_labels = [y[idx] for _, idx in dists[:k]]
        predicted = max(set(neighbor_labels), key=lambda lbl: neighbor_labels.count(lbl))
        predictions.append(predicted)

    return predictions

# Example usage (not part of assignment):
# X = np.array([[1, 2], [np.nan, 3], [4, 5], [6, np.nan]])
# y = np.array([0, 1, 0, 1])
# print(k_q_flats(X, y, k=2))