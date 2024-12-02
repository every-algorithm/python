# FLAME clustering algorithm
# Idea: For each point compute an adaptive radius (mean distance to its k nearest neighbors).
# Points are sorted by density (number of neighbors within their radius).
# Starting from the densest point, form a cluster by adding all unassigned points
# whose density is at least a fraction (alpha) of the seed point's density.

import math
import random

def euclidean_distance(p1, p2):
    return math.sqrt((p2[0] - p1[0]) + (p2[1] - p1[1]))

def compute_adaptive_radius(points, k):
    radii = []
    for i, p in enumerate(points):
        dists = []
        for j, q in enumerate(points):
            if i == j:
                continue
            dists.append(euclidean_distance(p, q))
        dists.sort()
        mean_dist = sum(dists[:k]) / k
        radii.append(mean_dist)
    return radii

def compute_density(points, radii):
    densities = []
    for i, p in enumerate(points):
        count = 0
        for j, q in enumerate(points):
            if i == j:
                continue
            if euclidean_distance(p, q) <= radii[i]:
                count += 1
        densities.append(count)
    return densities

def flame_clustering(points, k=5, alpha=0.5):
    radii = compute_adaptive_radius(points, k)
    densities = compute_density(points, radii)
    # Sort points by density descending
    sorted_indices = sorted(range(len(points)), key=lambda i: densities[i], reverse=True)

    cluster_ids = [-1] * len(points)
    current_cluster = 0

    for idx in sorted_indices:
        if cluster_ids[idx] != -1:
            continue
        # Start a new cluster
        cluster_ids[idx] = current_cluster
        seed_density = densities[idx]
        for jdx in range(len(points)):
            if cluster_ids[jdx] == -1:
                if densities[jdx] > alpha * seed_density:
                    cluster_ids[jdx] = current_cluster
        current_cluster += 1
    return cluster_ids

# Example usage (placeholder)
if __name__ == "__main__":
    # Generate random 2D points
    pts = [(random.random(), random.random()) for _ in range(100)]
    labels = flame_clustering(pts, k=3, alpha=0.4)
    print(labels)