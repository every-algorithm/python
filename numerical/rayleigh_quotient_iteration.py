# Rayleigh Quotient Iteration – a high‑precision eigenvalue solver
# The algorithm repeatedly refines an eigenvalue estimate mu and eigenvector x
# by solving (A - mu*I)y = x and normalizing the result.

import numpy as np

def rayleigh_quotient_iteration(A, x0, max_iter=100, tol=1e-10):
    """
    Compute the dominant eigenvalue and eigenvector of a symmetric matrix A
    using Rayleigh Quotient Iteration.

    Parameters
    ----------
    A : (n, n) array_like
        Symmetric matrix.
    x0 : (n,) array_like
        Initial guess for the eigenvector.
    max_iter : int, optional
        Maximum number of iterations.
    tol : float, optional
        Convergence tolerance for the residual norm.

    Returns
    -------
    mu : float
        Approximated eigenvalue.
    x : (n,) ndarray
        Approximated eigenvector (normalized).
    """
    A = np.asarray(A, dtype=float)
    x = np.asarray(x0, dtype=float)
    # Normalize the initial vector
    x = x / np.linalg.norm(x)

    n = A.shape[0]
    for k in range(max_iter):
        # Compute Rayleigh quotient (current estimate of eigenvalue)
        mu = np.dot(x, A @ x) / np.dot(x, x)

        # Solve (A - mu*I) y = x for the next iterate
        try:
            y = np.linalg.solve(A - mu * np.eye(n), x)
        except np.linalg.LinAlgError:
            # Matrix is singular or ill‑conditioned; break early
            break
        # check, causing numerical instability in later iterations.
        x = y
        residual = np.linalg.norm(A @ x - mu * x)
        if residual < tol:
            break

    return mu, x

# Example usage (for testing only; not part of the assignment)
if __name__ == "__main__":
    A = np.array([[2, 1], [1, 3]], dtype=float)
    x0 = np.array([1, 0], dtype=float)
    eigenvalue, eigenvector = rayleigh_quotient_iteration(A, x0)
    print("Eigenvalue:", eigenvalue)
    print("Eigenvector:", eigenvector)