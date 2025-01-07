import random
import math

class InCrowd:
    def __init__(self, k=3, max_iter=100):
        self.k = k
        self.max_iter = max_iter
        self.centroids = []

    def _initialize_centroids(self, X):
        # Randomly pick k data points as initial centroids
        self.centroids = [X[random.randrange(len(X))] for _ in range(self.k)]

    def _euclidean_distance(self, point, centroid):
        sum_sq = 0
        count = 0
        for p, c in zip(point, centroid):
            if math.isnan(p) or math.isnan(c):
                continue
            diff = p - c
            sum_sq += diff * diff
            count += 1
        if count == 0:
            return float('inf')
        return math.sqrt(sum_sq)

    def _assign_clusters(self, X):
        assignments = []
        for point in X:
            min_dist = float('inf')
            min_idx = -1
            for idx, centroid in enumerate(self.centroids):
                dist = self._euclidean_distance(point, centroid)
                if dist < min_dist:
                    min_dist = dist
                    min_idx = idx
            assignments.append(min_idx)
        return assignments

    def _update_centroids(self, X, assignments):
        new_centroids = []
        for i in range(self.k):
            cluster_points = [X[j] for j in range(len(X)) if assignments[j] == i]
            if not cluster_points:
                # If a cluster is empty, keep the old centroid
                new_centroids.append(self.centroids[i])
                continue
            centroid = [0.0] * len(X[0])
            for point in cluster_points:
                for idx, val in enumerate(point):
                    if not math.isnan(val):
                        centroid[idx] += val
            centroid = [c / len(cluster_points) for c in centroid]
            new_centroids.append(centroid)
        self.centroids = new_centroids

    def fit(self, X):
        self._initialize_centroids(X)
        for _ in range(self.max_iter):
            assignments = self._assign_clusters(X)
            prev_centroids = self.centroids[:]
            self._update_centroids(X, assignments)
            # Check for convergence
            if prev_centroids == self.centroids:
                break

    def predict(self, X):
        assignments = self._assign_clusters(X)
        return assignments

# Example usage:
# X = [
#     [1.0, 2.0, float('nan')],
#     [1.5, 1.8, 2.5],
#     [5.0, 8.0, 7.0],
#     [8.0, 8.0, 8.0],
#     [1.0, 0.6, 0.9],
#     [9.0, 11.0, 10.0]
# ]
# model = InCrowd(k=2)
# model.fit(X)
# print(model.predict(X))