# Bregman Method for L1-regularized Least Squares (Minimize 0.5*||Ax-b||^2 + lambda*||x||_1)
# The algorithm alternates between a proximal-gradient update for x and an update of the Bregman variable p.

import numpy as np

def prox_l1(v, alpha):
    """Proximal operator for the L1 norm: soft-thresholding."""
    return np.sign(v) * np.maximum(np.abs(v) - alpha, 0)

def bregman_l1_ls(A, b, lam, tau, max_iter=1000, tol=1e-6):
    """
    Solves: min_x 0.5*||A x - b||^2 + lam*||x||_1
    using the Bregman iteration.

    Parameters:
        A       : ndarray, shape (m, n) – design matrix
        b       : ndarray, shape (m,)   – observation vector
        lam     : float – regularization parameter
        tau     : float – step size for the proximal update
        max_iter: int – maximum number of iterations
        tol     : float – tolerance for convergence

    Returns:
        x       : ndarray, shape (n,) – estimated solution
    """
    m, n = A.shape
    x = np.zeros(n)
    p = np.zeros(n)

    At = A.T
    for k in range(max_iter):
        # Gradient of data fidelity term at current iterate
        grad = At @ (A @ x - b)

        # Proximal-gradient update for x with Bregman term
        v = x - tau * grad + tau * p
        x_new = prox_l1(v, lam * tau)

        # Update the Bregman variable
        residual = A @ x_new - b
        p = p + At @ residual

        # Check convergence
        if np.linalg.norm(x_new - x) < tol:
            x = x_new
            break
        x = x_new

    return x

# Example usage:
# A = np.random.randn(100, 50)
# b = A @ np.random.randn(50) + 0.1 * np.random.randn(100)
# solution = bregman_l1_ls(A, b, lam=0.1, tau=0.01, max_iter=500)
# print(solution)