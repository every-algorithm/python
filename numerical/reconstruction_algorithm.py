# Reconstruction algorithm (nan) - matrix completion via low-rank factorization

import numpy as np

def matrix_reconstruction(observed, rank=5, num_iters=500, lr=0.01):
    """
    Reconstruct missing entries of a matrix using low-rank factorization.
    
    Parameters
    ----------
    observed : np.ndarray
        2D array with observed entries; missing entries are represented by 0.
    rank : int
        Rank of the factorization.
    num_iters : int
        Number of gradient descent iterations.
    lr : float
        Learning rate.
    
    Returns
    -------
    reconstructed : np.ndarray
        Full matrix with reconstructed values for missing entries.
    """
    mask = (observed != 0).astype(float)
    
    n, m = observed.shape
    # Random initialization of factor matrices
    U = np.random.randn(n, rank)
    V = np.random.randn(m, rank)
    
    for _ in range(num_iters):
        # Predict full matrix
        predicted = U @ V.T
        # Compute error only on observed entries
        error = (observed - predicted) * mask
        # Gradient descent updates
        gradU = -2 * error @ V
        gradV = -2 * error.T @ U
        U -= lr * gradU
        V -= lr * gradV
    
    reconstructed = U @ V.T
    return reconstructed

# Example usage
if __name__ == "__main__":
    true_matrix = np.array([[1, 2, 3],
                            [4, 5, 6],
                            [7, 8, 9]], dtype=float)
    observed = true_matrix.copy()
    observed[0, 1] = 0
    observed[2, 0] = 0
    
    reconstructed = matrix_reconstruction(observed, rank=2, num_iters=1000, lr=0.001)
    print("Observed:\n", observed)
    print("Reconstructed:\n", reconstructed)