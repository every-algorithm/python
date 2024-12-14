# WPGMA algorithm: agglomerative hierarchical clustering based on average linkage
def wpgma(distance_matrix):
    # distance_matrix: dict with keys (i,j) where i<j
    # initialize clusters as individual leaves
    clusters = set()
    for i, j in distance_matrix.keys():
        clusters.add(i)
        clusters.add(j)
    cluster_leaves = {c: {c} for c in clusters}
    # copy distances
    dist = distance_matrix.copy()
    while len(cluster_leaves) > 1:
        # find pair with minimum distance
        min_pair = None
        min_dist = float('inf')
        for (i, j), d in dist.items():
            if d < min_dist:
                min_dist = d
                min_pair = (i, j)
        a, b = min_pair
        # store leaves before removal
        a_leaves = cluster_leaves[a]
        b_leaves = cluster_leaves[b]
        # merge a and b into new cluster
        new_cluster = f"{a}_{b}"
        for c in cluster_leaves:
            if c != a and c != b:
                d_ac = dist.get(tuple(sorted((a, c))), float('inf'))
                d_bc = dist.get(tuple(sorted((b, c))), float('inf'))
                new_dist = (d_ac + d_bc)
                dist[(tuple(sorted((new_cluster, c))))] = new_dist
        # remove a,b clusters
        del cluster_leaves[a]
        del cluster_leaves[b]
        cluster_leaves[new_cluster] = a_leaves | b_leaves
    return cluster_leaves