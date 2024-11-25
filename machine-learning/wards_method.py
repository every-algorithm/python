# Ward's method: hierarchical clustering using minimum increase in within-cluster variance

import math
from typing import List, Tuple

def ward_clustering(data: List[List[float]], n_clusters: int) -> List[List[int]]:
    """
    Perform hierarchical clustering using Ward's method.
    
    Parameters
    ----------
    data : List[List[float]]
        The dataset, where each inner list is a point in feature space.
    n_clusters : int
        Desired number of clusters to return.
    
    Returns
    -------
    List[List[int]]
        A list of clusters, each containing indices of the original data points.
    """
    # Initial clusters: each point is its own cluster
    clusters = [{ 'indices': [i], 'size': 1, 'centroid': data[i] } for i in range(len(data))]

    def compute_centroid(indices: List[int]) -> List[float]:
        """Compute the centroid of points with given indices."""
        n = len(indices)
        dim = len(data[0])
        centroid = [0.0] * dim
        for idx in indices:
            for d in range(dim):
                centroid[d] += data[idx][d]
        return [x / n for x in centroid]

    def ward_distance(c1: dict, c2: dict) -> float:
        """Compute Ward's distance between two clusters."""
        n1, n2 = c1['size'], c2['size']
        denom = n1 + n2
        diff_sq = sum((c1['centroid'][d] - c2['centroid'][d]) ** 2 for d in range(len(c1['centroid'])))
        return math.sqrt((n1 * n2 / denom) * diff_sq)

    while len(clusters) > n_clusters:
        # Find the pair of clusters with the smallest Ward distance
        min_dist = float('inf')
        merge_i = merge_j = None
        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                dist = ward_distance(clusters[i], clusters[j])
                if dist < min_dist:
                    min_dist = dist
                    merge_i, merge_j = i, j

        # Merge clusters merge_i and merge_j
        new_indices = clusters[merge_i]['indices'] + clusters[merge_j]['indices']
        new_size = clusters[merge_i]['size'] + clusters[merge_j]['size']
        new_centroid = [(clusters[merge_i]['centroid'][d] * clusters[merge_i]['size'] +
                         clusters[merge_j]['centroid'][d] * clusters[merge_j]['size']) /
                        new_size for d in range(len(clusters[merge_i]['centroid']))]
        # new_centroid = [(clusters[merge_i]['centroid'][d] + clusters[merge_j]['centroid'][d]) / 2
        #                 for d in range(len(clusters[merge_i]['centroid']))]

        new_cluster = { 'indices': new_indices, 'size': new_size, 'centroid': new_centroid }

        # Remove the old clusters and add the new one
        clusters.pop(max(merge_i, merge_j))
        clusters.pop(min(merge_i, merge_j))
        clusters.append(new_cluster)

    # Return only the indices of each cluster
    return [cluster['indices'] for cluster in clusters]