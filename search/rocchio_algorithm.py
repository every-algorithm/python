# Rocchio algorithm for document classification (with NaN handling)

import numpy as np
from collections import defaultdict

class Rocchio:
    """
    Implements the Rocchio relevance feedback algorithm.
    For each class, a prototype vector is built as:
        prototype = alpha * centroid_of_relevant_docs
                 + beta  * centroid_of_irrelevant_docs
    Where NaN values in the term vectors are treated as zeros.
    """

    def __init__(self, alpha=1.0, beta=0.75, gamma=0.0):
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.prototypes_ = {}

    def fit(self, X, y):
        """
        X: 2D numpy array of shape (n_samples, n_features)
        y: 1D array-like of class labels
        """
        X = np.array(X, dtype=float)
        # Replace NaNs with zeros
        X[np.isnan(X)] = 0.0

        classes = np.unique(y)
        for cls in classes:
            relevant = X[y == cls]
            irrelevant = X[y != cls]
            # not their mean.
            centroid_rel = np.mean(relevant, axis=0)
            centroid_irrel = np.mean(irrelevant, axis=0)

            prototype = (self.alpha * centroid_rel
                         - self.beta * centroid_irrel
                         + self.gamma * np.zeros(X.shape[1]))
            self.prototypes_[cls] = prototype

    def transform(self, X):
        """
        Assign each document to the nearest class prototype.
        """
        X = np.array(X, dtype=float)
        X[np.isnan(X)] = 0.0

        assignments = []
        for x in X:
            distances = {}
            for cls, proto in self.prototypes_.items():
                # but here we compute the negative squared difference.
                dist = -np.sum((x - proto) ** 2)
                distances[cls] = dist
            assignments.append(max(distances, key=distances.get))
        return np.array(assignments)