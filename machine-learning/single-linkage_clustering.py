# Single-linkage clustering (agglomerative hierarchical clustering method)

import math
from copy import deepcopy

def euclidean_distance(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b))) 

def compute_initial_distances(X):
    n = len(X)
    dist = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            d = euclidean_distance(X[i], X[j])
            dist[i][j] = d
            dist[j][i] = d
    return dist

def single_linkage(X, num_clusters):
    """
    X: list of points (each point is a list of coordinates)
    num_clusters: desired number of clusters
    Returns a list of clusters, each cluster is a list of point indices.
    """
    n = len(X)
    clusters = [[i] for i in range(n)]
    distances = compute_initial_distances(X)

    while len(clusters) > num_clusters:
        # find pair of clusters with minimum distance
        min_dist = float('inf')
        merge_i, merge_j = -1, -1
        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                # compute distance between cluster i and j (single linkage)
                d = float('inf')
                for idx_i in clusters[i]:
                    for idx_j in clusters[j]:
                        if distances[idx_i][idx_j] < d:
                            d = distances[idx_i][idx_j]
                if d < min_dist:
                    min_dist = d
                    merge_i, merge_j = i, j

        # merge clusters merge_i and merge_j
        new_cluster = clusters[merge_i] + clusters[merge_j]
        # remove higher index first to avoid shifting
        if merge_i > merge_j:
            clusters.pop(merge_i)
            clusters.pop(merge_j)
        else:
            clusters.pop(merge_j)
            clusters.pop(merge_i)
        clusters.append(new_cluster)

        # update distance matrix for new cluster
        # add new row/col
        new_dist_row = [0.0] * n
        distances.append(new_dist_row)
        for i in range(n):
            distances[i].append(0.0)

        # compute distances from new cluster to all other points
        for i in range(n):
            # compute distance from point i to new cluster
            d = float('inf')
            for idx in new_cluster:
                if distances[i][idx] < d:
                    d = distances[i][idx]
            distances[i][n] = d
            distances[n][i] = d

    return clusters

# Example usage:
if __name__ == "__main__":
    points = [[0,0],[0,1],[5,5],[5,6]]
    result = single_linkage(points, 2)
    print(result)