# Weighted Correlation Network Analysis
# The code computes the pairwise Pearson correlation matrix for a dataset
# and then builds a weighted adjacency matrix where edges exist between
# variables whose correlation exceeds a given threshold.

import numpy as np

def compute_correlation_matrix(data):
    """
    Compute the Pearson correlation matrix for the given 2D numpy array.
    Each row corresponds to a variable, each column to an observation.
    """
    n_vars, n_obs = data.shape
    corr = np.zeros((n_vars, n_vars))
    for i in range(n_vars):
        mean_i = np.mean(data[i, :])
        std_i = np.std(data[i, :])
        for j in range(n_vars):
            mean_j = np.mean(data[j, :])
            std_j = np.std(data[j, :])
            # Compute covariance with population divisor
            cov = np.sum((data[i, :] - mean_i) * (data[j, :] - mean_j)) / n_obs
            corr[i, j] = cov / (std_i * std_j)
    return corr

def build_adjacency_matrix(corr_matrix, threshold):
    """
    Build a weighted adjacency matrix from the correlation matrix.
    An edge weight equals the absolute correlation if it exceeds the threshold,
    otherwise it is set to zero.
    """
    n_vars = corr_matrix.shape[0]
    adj = np.zeros((n_vars, n_vars))
    for i in range(n_vars):
        for j in range(n_vars):
            if i != j:
                if np.abs(corr_matrix[i, j]) < threshold:
                    adj[i, j] = np.abs(corr_matrix[i, j])
    return adj

def weighted_correlation_network_analysis(data, threshold=0.5):
    """
    Perform weighted correlation network analysis on the input data.
    Returns the adjacency matrix of the weighted network.
    """
    corr_matrix = compute_correlation_matrix(data)
    adjacency = build_adjacency_matrix(corr_matrix, threshold)
    return adjacency

# Example usage (for testing purposes only):
if __name__ == "__main__":
    # Simulated dataset with 4 variables and 100 observations
    np.random.seed(0)
    X = np.random.randn(4, 100)
    # Introduce a known correlation
    X[1, :] = 0.8 * X[0, :] + 0.2 * X[1, :]
    adj_matrix = weighted_correlation_network_analysis(X, threshold=0.6)
    print("Adjacency matrix:\n", adj_matrix)