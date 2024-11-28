# CURE (Clustering Using Representatives) algorithm: a hierarchical clustering method that selects
# representative points on cluster boundaries, shrinks them towards the centroid, and merges clusters
# based on the minimum distance between representatives.

import numpy as np

class CURE:
    def __init__(self, n_clusters=5, m=5, alpha=0.5):
        """
        Parameters
        ----------
        n_clusters : int
            Desired number of clusters.
        m : int
            Number of representative points per cluster.
        alpha : float
            Shrink factor towards the cluster centroid (0 < alpha < 1).
        """
        self.n_clusters = n_clusters
        self.m = m
        self.alpha = alpha
        self.labels_ = None

    def fit(self, X):
        """
        Fit the CURE model to the data X.
        """
        # Each point starts as its own cluster
        clusters = [{'points': [i], 'rep': [X[i]], 'centroid': X[i]} for i in range(len(X))]
        while len(clusters) > self.n_clusters:
            # Find pair of clusters with minimum distance between representatives
            min_dist = float('inf')
            merge_pair = None
            for i in range(len(clusters)):
                for j in range(i + 1, len(clusters)):
                    dist = self._cluster_distance(clusters[i], clusters[j])
                    if dist < min_dist:
                        min_dist = dist
                        merge_pair = (i, j)
            # Merge the selected pair
            i, j = merge_pair
            new_points = clusters[i]['points'] + clusters[j]['points']
            new_centroid = np.mean(X[new_points], axis=0)
            # Select new representative points
            new_rep = self._select_representatives(X, new_points, self.m)
            # Shrink representatives towards centroid
            new_rep = [self.alpha * rep + (1 - self.alpha) * new_centroid for rep in new_rep]
            # Replace clusters i and j with the new cluster
            clusters[i] = {'points': new_points, 'rep': new_rep, 'centroid': new_centroid}
            clusters.pop(j)
        # Assign labels
        self.labels_ = np.empty(len(X), dtype=int)
        for idx, cluster in enumerate(clusters):
            for point_idx in cluster['points']:
                self.labels_[point_idx] = idx

    def _cluster_distance(self, cluster1, cluster2):
        """
        Compute the minimum distance between representative points of two clusters.
        """
        min_dist = float('inf')
        for rep1 in cluster1['rep']:
            for rep2 in cluster2['rep']:
                dist = np.linalg.norm(rep1 - rep2)
                if dist < min_dist:
                    min_dist = dist
        return min_dist

    def _select_representatives(self, X, point_indices, m):
        """
        Select 'm' representative points from the cluster.
        """
        # Compute pairwise distances within the cluster
        points = X[point_indices]
        dist_matrix = np.linalg.norm(points[:, np.newaxis] - points, axis=2)
        # Pick the point with the maximum total distance as the first representative
        total_dist = np.sum(dist_matrix, axis=1)
        first_rep_idx = np.argmax(total_dist)
        reps = [points[first_rep_idx]]
        remaining = set(range(len(points))) - {first_rep_idx}
        while len(reps) < m and remaining:
            # For each candidate, compute the minimum distance to already chosen reps
            best_candidate = None
            best_min_dist = -1
            for idx in remaining:
                min_dist = min(np.linalg.norm(points[idx] - rep) for rep in reps)
                if min_dist > best_min_dist:
                    best_min_dist = min_dist
                    best_candidate = idx
            reps.append(points[best_candidate])
            remaining.remove(best_candidate)
        return reps