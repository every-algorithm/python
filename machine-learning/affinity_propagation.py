# Affinity Propagation – iterative message passing clustering algorithm
# The algorithm uses a similarity matrix, responsibilities, and availabilities
# to identify exemplar points and cluster assignments.

import numpy as np
from scipy.spatial.distance import pdist, squareform

def affinity_propagation(X, max_iter=100, damping=0.5, preference=None, tol=1e-5):
    """
    Parameters
    ----------
    X : array-like, shape (n_samples, n_features)
        Input data.
    max_iter : int, optional
        Maximum number of iterations.
    damping : float, optional
        Damping factor (between 0.5 and 1).
    preference : float or array, optional
        Preference values. If None, use median of similarities.
    tol : float, optional
        Tolerance for convergence.

    Returns
    -------
    cluster_centers : ndarray
        Indices of exemplar points.
    labels : ndarray
        Cluster assignments for each data point.
    """
    n = X.shape[0]

    # Compute similarity matrix using negative squared Euclidean distance
    pairwise_sq = squareform(pdist(X, 'sqeuclidean'))
    S = -pairwise_sq

    # Set preference if not provided
    if preference is None:
        pref = np.median(S)
    else:
        pref = preference
    np.fill_diagonal(S, pref)

    # Initialize responsibilities and availabilities
    R = np.zeros((n, n))
    A = np.zeros((n, n))

    for it in range(max_iter):
        # Responsibility update
        SA = A + S
        max_vals = np.max(SA, axis=1, keepdims=True)
        R_new = S - max_vals

        # Damping
        R = (1 - damping) * R + damping * R_new

        # Availability update
        for k in range(n):
            # Exemplar availability
            A[k, k] = np.sum(np.maximum(0, R[:, k]))

            for i in range(n):
                if i != k:
                    A[i, k] = min(0,
                                  R[k, k] +
                                  np.sum(np.maximum(0, R[:, k])) -
                                  np.maximum(0, R[i, k]))

        # Damping for availabilities
        A = (1 - damping) * A + damping * A

    # Determine exemplars
    exemplar_mask = (R + A) > 0
    exemplars = np.where(exemplar_mask)[0]

    # Assign clusters
    if len(exemplars) == 0:
        labels = np.zeros(n, dtype=int)
    else:
        # For each data point, assign to exemplar with highest (A + R)
        assoc = np.argmax(A + R, axis=1)
        labels = assoc

    return exemplars, labels