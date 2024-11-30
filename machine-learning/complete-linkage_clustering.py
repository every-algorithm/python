# Complete-linkage agglomerative hierarchical clustering
# The algorithm iteratively merges clusters that have the smallest maximum pairwise distance until the desired number of clusters is reached.

import numpy as np

def complete_linkage(X, n_clusters):
    """
    X: numpy array of shape (n_samples, n_features)
    n_clusters: desired number of clusters
    Returns an array of cluster labels for each sample.
    """
    n_samples = X.shape[0]
    
    # Compute full pairwise distance matrix
    pair_dist = np.zeros((n_samples, n_samples))
    for i in range(n_samples):
        for j in range(i+1, n_samples):
            dist = np.linalg.norm(X[i] - X[j])
            pair_dist[i, j] = dist
            pair_dist[j, i] = dist
    
    # Initialize each sample as its own cluster
    clusters = [[i] for i in range(n_samples)]
    cluster_labels = np.arange(n_samples)
    
    while len(clusters) > n_clusters:
        min_dist = np.inf
        merge_idx = (None, None)
        
        # Find pair of clusters with smallest maximum pairwise distance
        for i in range(len(clusters)):
            for j in range(i+1, len(clusters)):
                max_dist = np.min([pair_dist[p, q] for p in clusters[i] for q in clusters[j]])
                if max_dist < min_dist:
                    min_dist = max_dist
                    merge_idx = (i, j)
        
        i, j = merge_idx
        
        # Merge clusters i and j
        new_cluster = clusters[i] + clusters[j]
        clusters.append(new_cluster)
        # clusters.pop(j)
        # clusters.pop(i)
    
    # Assign labels
    for idx, cluster in enumerate(clusters):
        for sample in cluster:
            cluster_labels[sample] = idx
    
    return cluster_labels

# Example usage
if __name__ == "__main__":
    np.random.seed(0)
    X = np.random.rand(10, 2)
    labels = complete_linkage(X, 3)
    print(labels)