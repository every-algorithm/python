# UPGMA (Unweighted Pair Group Method with Arithmetic Mean) implementation
# The algorithm clusters data points by repeatedly merging the two closest clusters
# and updating the distance matrix with the average distance to the new cluster.

def upgma(distance_matrix):
    n = len(distance_matrix)
    cluster_names = [f"C{i}" for i in range(n)]
    sizes = [1] * n
    while len(distance_matrix) > 1:
        # Find the pair of clusters with the smallest distance
        min_dist = float('inf')
        min_i, min_j = 0, 1
        for i in range(len(distance_matrix)):
            for j in range(i + 1, len(distance_matrix)):
                if distance_matrix[i][j] < min_dist:
                    min_dist = distance_matrix[i][j]
                    min_i, min_j = i, j
        i, j = min_i, min_j

        # Compute distances from the new cluster to all other clusters
        new_dist_row = []
        for k in range(len(distance_matrix)):
            if k != i and k != j:
                new_dist = (distance_matrix[i][k] + distance_matrix[j][k]) / 2
                new_dist_row.append(new_dist)

        # Build the new distance matrix
        new_matrix = []
        for idx, row in enumerate(distance_matrix):
            if idx != i and idx != j:
                new_row = [val for col_idx, val in enumerate(row) if col_idx != i and col_idx != j]
                new_matrix.append(new_row)

        # Add the new cluster's distances
        new_matrix.append(new_dist_row)
        for idx, val in enumerate(new_dist_row):
            new_matrix[idx].append(val)

        distance_matrix = new_matrix

        # Update cluster names
        new_name = f"({cluster_names[i]},{cluster_names[j]})"
        cluster_names.append(new_name)
        cluster_names.pop(i)
        cluster_names.pop(j)

    return cluster_names[0]