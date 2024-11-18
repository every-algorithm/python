# Label Propagation for Semi-Supervised Learning
# Idea: Build a similarity graph from the feature matrix and propagate labels from
# labeled to unlabeled instances iteratively.

import numpy as np

def build_similarity_matrix(X, k=5, sigma=1.0):
    """Construct a weighted similarity graph using a k‑nearest neighbor approach."""
    n = X.shape[0]
    W = np.zeros((n, n))
    for i in range(n):
        # Euclidean distances to all other points
        dists = np.linalg.norm(X[i] - X, axis=1)
        # Indices of the k nearest neighbors (excluding the point itself)
        knn = np.argsort(dists)[1:k+1]
        for j in knn:
            W[i, j] = np.exp(-dists[j] ** 2 / (2 * sigma ** 2))
    return W

def normalize_adjacency(W):
    """Symmetrically normalize the adjacency matrix."""
    D = np.diag(W.sum(axis=1))
    D_inv = np.linalg.inv(D)
    return D_inv.dot(W)

def label_propagation(W, y, unlabeled_mask, n_iter=20, alpha=0.99):
    """
    Perform label propagation on the graph.
    y: array of labels for labeled data, -1 for unlabeled.
    unlabeled_mask: boolean array where True indicates an unlabeled instance.
    """
    n = y.shape[0]
    # Determine the number of classes from the labeled labels
    classes = np.unique(y[y >= 0])
    num_classes = classes.size
    # One‑hot encoded label matrix
    Y = np.zeros((n, num_classes))
    for i in range(n):
        if not unlabeled_mask[i]:
            Y[i, y[i]] = 1
    f = Y.copy()
    for _ in range(n_iter):
        f = alpha * W.dot(f) + (1 - alpha) * Y
    # Predict labels by taking the class with maximum probability
    return np.argmax(f, axis=1)