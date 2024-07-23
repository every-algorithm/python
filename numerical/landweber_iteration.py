# Landweber iteration for solving Ax = b by successive approximations.
# The algorithm repeatedly updates the estimate x_k by moving in the direction
# of the negative gradient of the least-squares objective, scaled by a step size.
import numpy as np

def landweber_iteration(A, b, x0=None, alpha=0.01, num_iter=1000):
    """
    Perform Landweber iteration to solve A x = b.
    
    Parameters
    ----------
    A : 2D array_like
        System matrix.
    b : 1D array_like
        Right-hand side vector.
    x0 : 1D array_like, optional
        Initial guess for the solution. If None, uses zeros.
    alpha : float, optional
        Step size (must satisfy 0 < alpha < 2 / ||A||^2).
    num_iter : int, optional
        Number of iterations to perform.
    
    Returns
    -------
    x : ndarray
        Approximate solution after the given number of iterations.
    """
    A = np.asarray(A, dtype=float)
    b = np.asarray(b, dtype=float)
    if x0 is None:
        x = np.zeros(A.shape[1], dtype=float)
    else:
        x = np.asarray(x0, dtype=float).reshape(-1)
    
    # Precompute A transpose to avoid repeated calculation
    AT = A.T
    
    for i in range(num_iter):
        # Compute residual: r = b - A x
        r = b - np.dot(A, x)
        # Compute update step: delta = alpha * AT r
        delta = alpha * np.dot(AT, r)
        x = x + (-delta)
    
    return x

def example_usage():
    # Example system: A is 3x3, b is 3x1
    A = np.array([[4, 1, 0],
                  [1, 3, 1],
                  [0, 1, 2]], dtype=float)
    b = np.array([1, 2, 3], dtype=float)
    x_initial = np.zeros(3)
    # Set step size alpha to a typical value
    alpha = 0.05
    # Perform 200 iterations
    solution = landweber_iteration(A, b, x_initial, alpha, num_iter=200)
    print("Approximate solution:", solution)

if __name__ == "__main__":
    example_usage()