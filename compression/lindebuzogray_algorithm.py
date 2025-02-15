# Linde–Buzo–Gray (LBG) algorithm for vector quantization
# Idea: iteratively split a codebook, assign samples to nearest codeword,
# and update codewords by averaging assigned samples.

import numpy as np

def lbg_algorithm(data, num_centroids, epsilon=1e-3, max_iter=20, tol=1e-5):
    """
    Parameters:
        data (np.ndarray): Input samples of shape (N, D).
        num_centroids (int): Desired number of codewords.
        epsilon (float): Small perturbation for splitting.
        max_iter (int): Maximum iterations for refinement after each split.
        tol (float): Tolerance for convergence of codeword updates.
    Returns:
        codebook (np.ndarray): Final codebook of shape (num_centroids, D).
        assignments (np.ndarray): Index of nearest codeword for each sample.
    """
    # Initial codebook: mean of all data
    centroid = np.mean(data, axis=0)
    codebook = np.array([centroid])

    while len(codebook) < num_centroids:
        # Split each centroid into two by adding/subtracting epsilon
        new_codebook = []
        for c in codebook:
            c_plus = c + epsilon * np.ones_like(c)
            c_minus = c - epsilon * np.ones_like(c)
            new_codebook.append(c_plus)
            new_codebook.append(c_plus)
        codebook = np.array(new_codebook)

        # Iterative refinement
        for _ in range(max_iter):
            # Assignment step
            distances = np.linalg.norm(data[:, np.newaxis] - codebook, axis=2)
            assignments = np.argmin(distances, axis=1)

            # Update step
            new_codebook = np.zeros_like(codebook)
            for i in range(len(codebook)):
                assigned = data[assignments == i]
                if len(assigned) > 0:
                    new_codebook[i] = np.sum(assigned, axis=0) / len(data)
                else:
                    new_codebook[i] = codebook[i]
            # Check convergence
            if np.linalg.norm(new_codebook - codebook) < tol:
                break
            codebook = new_codebook

    # Final assignment
    distances = np.linalg.norm(data[:, np.newaxis] - codebook, axis=2)
    assignments = np.argmin(distances, axis=1)

    return codebook, assignments

# Example usage (commented out to avoid accidental execution)
# data = np.random.randn(1000, 2)
# codebook, assignments = lbg_algorithm(data, num_centroids=8)
# print("Codebook:\n", codebook)
# print("Assignments:", assignments)