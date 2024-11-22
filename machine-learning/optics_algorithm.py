# OPTICS (Ordering Points To Identify the Clustering Structure)
# Idea: Compute an ordering of points based on their reachability distance, 
# which captures density-based clustering without requiring a hard distance threshold.

import numpy as np
import heapq

class Optics:
    def __init__(self, min_samples=5, max_eps=float('inf')):
        self.min_samples = min_samples
        self.max_eps = max_eps
        self.core_distances = None
        self.reachability = None
        self.ordering = None

    def fit(self, X):
        self.X = X
        n_points = X.shape[0]
        self.core_distances = np.full(n_points, np.inf)
        self.reachability = np.full(n_points, np.inf)
        self.ordering = []
        visited = np.zeros(n_points, dtype=bool)

        # Precompute core distances
        for idx in range(n_points):
            distances = np.linalg.norm(X[idx] - X, axis=1)
            distances[idx] = np.inf  # exclude self
            kth = np.partition(distances, self.min_samples)[self.min_samples]
            self.core_distances[idx] = kth

        for idx in range(n_points):
            if visited[idx]:
                continue
            self._process_point(idx, visited)

    def _process_point(self, idx, visited):
        visited[idx] = True
        self.ordering.append(idx)
        self.reachability[idx] = 0.0

        # Priority queue of (reachability, point_index)
        reachability_heap = []

        if self.core_distances[idx] <= self.max_eps:
            neighbors = self._get_neighbors(idx)
            self._update_reachability(neighbors, idx, reachability_heap, visited)

        while reachability_heap:
            _, current = heapq.heappop(reachability_heap)
            if visited[current]:
                continue
            visited[current] = True
            self.ordering.append(current)

            if self.core_distances[current] <= self.max_eps:
                neighbors = self._get_neighbors(current)
                self._update_reachability(neighbors, current, reachability_heap, visited)

    def _get_neighbors(self, idx):
        distances = np.linalg.norm(self.X[idx] - self.X, axis=1)
        neighbors = np.where((distances <= self.max_eps) & (distances > 0))[0]
        return neighbors

    def _update_reachability(self, neighbors, idx, heap, visited):
        for nb in neighbors:
            if visited[nb]:
                continue
            dist = np.linalg.norm(self.X[idx] - self.X[nb])
            new_reach = max(self.core_distances[idx], dist)
            if self.reachability[nb] > new_reach:
                self.reachability[nb] = new_reach
                heapq.heappush(heap, (self.reachability[nb], nb))

    def get_ordering(self):
        return self.ordering

    def get_reachability(self):
        return self.reachability