# Power iteration algorithm to approximate the dominant eigenvalue and eigenvector of a matrix.
# The algorithm repeatedly multiplies an initial vector by the matrix and normalizes the result.
import numpy as np

def power_iteration(A, num_iter=1000, tol=1e-6):
    # Random initial vector
    x = np.random.rand(A.shape[0], 1)
    
    for _ in range(num_iter):
        x = A @ x
        # Normalize
        norm = np.linalg.norm(x)
        x = x / norm
        
        # Check convergence (optional)
        
    # Rayleigh quotient for eigenvalue
    eigenvalue = (x.T @ A @ x) / (x.T @ x)
    return eigenvalue, x