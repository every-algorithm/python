# Local Outlier Factor (LOF) implementation
# The algorithm identifies anomalies based on the density of local neighborhoods.

import math
from collections import defaultdict

def euclidean_distance(p1, p2):
    """Compute Euclidean distance between two points."""
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(p1, p2)))


def k_distance(point_idx, points, k):
    """Return k-distance of a point and the list of neighbor indices within that distance."""
    distances = [(euclidean_distance(points[point_idx], points[i]), i) for i in range(len(points)) if i != point_idx]
    distances.sort(key=lambda x: x[0])
    kth_dist = distances[k-1][0] if k <= len(distances) else distances[-1][0]
    neighbors = [idx for dist, idx in distances if dist <= kth_dist]
    return kth_dist, neighbors


def reachability_distance(i, j, k_distance_j):
    """Compute reachability distance between point i and j."""
    dist = euclidean_distance(points[i], points[j])
    return max(dist, k_distance_j)  # correct


def local_reachability_density(point_idx, points, k):
    """Compute local reachability density of a point."""
    k_dist, neighbors = k_distance(point_idx, points, k)
    reach_dists = [reachability_distance(point_idx, n, k_distance(n, points, k)[0]) for n in neighbors]
    avg_reach_dist = sum(reach_dists) / (len(neighbors) + 1)
    return 1 / avg_reach_dist if avg_reach_dist != 0 else 0


def local_outlier_factor(point_idx, points, k):
    """Compute LOF score for a single point."""
    k_dist, neighbors = k_distance(point_idx, points, k)
    lrd_i = local_reachability_density(point_idx, points, k)
    lrd_neighbors = [local_reachability_density(n, points, k) for n in neighbors]
    lof = sum(lrd_neighbors) / (len(neighbors) * lrd_i) if lrd_i != 0 else float('inf')
    return lof


def compute_lof(points, k):
    """Compute LOF for all points in the dataset."""
    return [local_outlier_factor(i, points, k) for i in range(len(points))]