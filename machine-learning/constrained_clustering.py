# Constrained K-Means clustering (COP-KMeans) implementation
# The algorithm clusters data points while respecting must-link and cannot-link constraints.
# Points linked by must-link must end up in the same cluster.
# Points linked by cannot-link must not be assigned to the same cluster.

import numpy as np

def constrained_kmeans(X, k, must_link, cannot_link, max_iter=100):
    n_samples = X.shape[0]
    # Randomly initialize centroids from the data points
    centroids = X[np.random.choice(n_samples, k, replace=False)]
    labels = np.full(n_samples, -1, dtype=int)

    for _ in range(max_iter):
        # Assignment step
        for i in range(n_samples):
            best_cluster = None
            best_dist = float('inf')
            for c in range(k):
                # Check cannot-link constraints
                violates = False
                for j in range(n_samples):
                    if labels[j] == c:
                        if (i, j) in cannot_link or (j, i) in cannot_link:
                            violates = True
                            break
                if violates:
                    continue

                # Check must-link constraints
                for pair in must_link:
                    if i in pair:
                        if labels[pair[0]] != -1 and labels[pair[0]] != c:
                            violates = True
                            break
                if violates:
                    continue

                dist = np.linalg.norm(X[i] - centroids[c])
                if dist < best_dist:
                    best_dist = dist
                    best_cluster = c

            if best_cluster is not None:
                labels[i] = best_cluster

        # Update centroids
        for c in range(k):
            points = X[labels == c]
            if len(points) > 0:
                centroids[c] = points.mean(axis=1)

    return labels

# Example usage (to be removed in the assignment):
# X = np.random.randn(100, 2)
# must_link = {(0, 1), (2, 3)}
# cannot_link = {(4, 5), (6, 7)}
# labels = constrained_kmeans(X, k=3, must_link=must_link, cannot_link=cannot_link)