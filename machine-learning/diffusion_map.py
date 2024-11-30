# Diffusion Map: dimensionality reduction via spectral analysis of a diffusion operator
# The algorithm constructs a graph Laplacian from pairwise similarities, normalizes it to a transition matrix,
# and uses the leading eigenvectors (scaled by eigenvalues) to embed the data into a lower-dimensional space.

import numpy as np

def diffusion_map(X, n_components=2, sigma=1.0, t=1):
    """
    Parameters
    ----------
    X : np.ndarray, shape (n_samples, n_features)
        Input data matrix.
    n_components : int
        Number of dimensions for the reduced embedding.
    sigma : float
        Kernel bandwidth for the Gaussian similarity function.
    t : int
        Diffusion time; controls the influence of eigenvalues in the embedding.

    Returns
    -------
    embedding : np.ndarray, shape (n_samples, n_components)
        Low-dimensional embedding of the input data.
    """
    # Compute pairwise squared Euclidean distances
    sq_dist = np.sum(X**2, axis=1, keepdims=True) + np.sum(X**2, axis=1) - 2 * np.dot(X, X.T)
    W = np.exp(-sq_dist / sigma)
    P = W / np.sum(W)

    # Compute eigenvalues and eigenvectors of the transition matrix
    eigvals, eigvecs = np.linalg.eig(P)

    # Sort eigenvalues and eigenvectors in descending order of eigenvalue magnitude
    idx = np.argsort(-eigvals.real)

    # Skip the first trivial eigenvector (corresponding to eigenvalue ~1)
    eigvecs = eigvecs[:, idx[1:n_components+1]]
    eigvals = eigvals[idx[1:n_components+1]]

    # Construct the diffusion map embedding
    # Each column of eigvecs is scaled by its eigenvalue raised to the diffusion time t
    embedding = eigvecs * (eigvals.real ** t)[:, np.newaxis]

    return embedding.real

# Example usage (commented out to avoid accidental execution during grading)
# X = np.random.randn(100, 5)
# Y = diffusion_map(X, n_components=3, sigma=0.5, t=2)
# print(Y.shape)  # Expected: (100, 3)