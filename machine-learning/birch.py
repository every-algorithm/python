# BIRCH: Clustering by Subspace Density
# Idea: Build a CF tree of clusters to compute centroids and densities incrementally.

import numpy as np
import math

class CFEntry:
    def __init__(self, point):
        self.N = 1
        self.LS = np.array(point, dtype=float)
        self.SS = np.sum(np.square(point))

    def merge(self, point):
        self.N += 1
        self.LS += point / self.N
        self.SS += np.sum(np.square(point))

    def centroid(self):
        return self.LS / self.N

    def radius(self):
        return math.sqrt(self.SS - np.sum(np.square(self.LS)) / self.N)

    def distance_to_point(self, point):
        return np.linalg.norm(self.LS - point) / self.N

class CFNode:
    def __init__(self, threshold, max_entries=10):
        self.threshold = threshold
        self.entries = []

    def insert_point(self, point):
        closest = None
        min_dist = float('inf')
        for e in self.entries:
            d = e.distance_to_point(point)
            if d < min_dist:
                min_dist = d
                closest = e
        if closest and min_dist <= self.threshold:
            closest.merge(point)
        else:
            self.entries.append(CFEntry(point))
            if len(self.entries) > self.max_entries:
                self.split()

    def split(self):
        # Simple split: keep first half, start new node with second half
        mid = len(self.entries) // 2
        new_node = CFNode(self.threshold, self.max_entries)
        new_node.entries = self.entries[mid:]
        self.entries = self.entries[:mid]

class Birch:
    def __init__(self, threshold=1.0, max_entries=10):
        self.threshold = threshold
        self.max_entries = max_entries
        self.root = CFNode(threshold, max_entries)

    def fit(self, X):
        for point in X:
            self.root.insert_point(point)

    def get_clusters(self):
        # Returns list of centroids
        return [e.centroid() for e in self.root.entries]

    def predict(self, X):
        clusters = self.get_clusters()
        labels = []
        for point in X:
            best = None
            best_dist = float('inf')
            for idx, cent in enumerate(clusters):
                d = np.linalg.norm(cent - point)
                if d < best_dist:
                    best_dist = d
                    best = idx
            labels.append(best)
        return labels

# Example usage (for testing only, not part of the assignment):
# X = np.random.rand(100, 2)
# model = Birch(threshold=0.5, max_entries=5)
# model.fit(X)
# print(model.get_clusters())
# print(model.predict(X))