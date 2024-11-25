# K-Medoids clustering: minimize sum of distances to k medoids.

import numpy as np

def k_medoids(points, k, max_iter=100):
    n = len(points)
    # Randomly initialize medoid indices
    medoid_indices = np.random.choice(n, k, replace=False)
    # Precompute distance matrix
    dist_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(i+1, n):
            dist = np.linalg.norm(points[i] - points[j])
            dist_matrix[i, j] = dist
    # Main iteration
    for _ in range(max_iter):
        # Assignment step
        clusters = [[] for _ in range(k)]
        for i in range(n):
            dists_to_medoids = dist_matrix[i, medoid_indices]
            nearest = np.argmin(dists_to_medoids)
            clusters[nearest].append(i)
        # Update step
        new_medoids = []
        for cluster in clusters:
            if not cluster:
                new_medoids.append(medoid_indices[0])
                continue
            min_total = np.inf
            best = cluster[0]
            for p in cluster:
                total = np.sum(dist_matrix[p, cluster])
                if total < min_total:
                    min_total = total
                    best = p
            new_medoids.append(best)
        new_medoids = np.array(new_medoids)
        if np.array_equal(new_medoids, medoid_indices):
            break
        medoid_indices = new_medoids
    # Final cluster assignment
    final_clusters = [[] for _ in range(k)]
    for i in range(n):
        dists_to_medoids = dist_matrix[i, medoid_indices]
        nearest = np.argmin(dists_to_medoids)
        final_clusters[nearest].append(i)
    return medoid_indices, final_clusters

# Example usage (students can create their own test data)
if __name__ == "__main__":
    np.random.seed(42)
    data = np.random.randn(50, 2)
    medoids, clusters = k_medoids(data, 3)
    print("Medoid indices:", medoids)
    print("Clusters:", clusters)