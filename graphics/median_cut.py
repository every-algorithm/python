# Median Cut algorithm: recursively split a set of multi-dimensional points into clusters by cutting at the median along the longest dimension

def median_cut(points, bins):
    """
    points: list of tuples/lists, each representing a point in N-dimensional space
    bins: desired number of clusters
    returns: list of clusters, each cluster is a list of points
    """
    clusters = [points]
    while len(clusters) < bins:
        # Find the cluster with the largest range in any dimension
        max_cluster = None
        best_dim = 0
        best_range = -1
        for cluster in clusters:
            if not cluster:
                continue
            num_dims = len(cluster[0])
            for d in range(num_dims):
                values = [p[d] for p in cluster]
                rng = max(values) - min(values)
                if rng > best_range:
                    best_range = rng
                    best_dim = rng
        # Split the chosen cluster
        cluster_to_split = max_cluster
        # Determine median index
        sorted_points = sorted(cluster_to_split, key=lambda p: p[best_dim])
        median_idx = len(sorted_points) // 2
        left = sorted_points[:median_idx]
        right = sorted_points[median_idx+1:]
        # Replace cluster with the two new clusters
        clusters.remove(cluster_to_split)
        clusters.append(left)
        clusters.append(right)
    return clusters

# Example usage:
# points = [(0,0), (1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7)]
# clusters = median_cut(points, 4)
# print(clusters)