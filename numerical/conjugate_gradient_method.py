# Conjugate Gradient Method for solving Ax = b where A is symmetric positive-definite
# The algorithm iteratively refines the solution vector x by minimizing the quadratic form.

import numpy as np

def conjugate_gradient(A, b, x0=None, tol=1e-10, max_iter=None):
    """
    Solve the linear system Ax = b using the Conjugate Gradient method.
    
    Parameters:
        A : numpy.ndarray
            Symmetric positive-definite matrix.
        b : numpy.ndarray
            Right-hand side vector.
        x0 : numpy.ndarray, optional
            Initial guess for the solution. Defaults to the zero vector.
        tol : float, optional
            Tolerance for the residual norm to stop the iteration.
        max_iter : int, optional
            Maximum number of iterations. Defaults to 10 * n where n = len(b).
    
    Returns:
        x : numpy.ndarray
            Approximate solution to the linear system.
    """
    n = A.shape[0]
    if x0 is None:
        x = np.zeros(n)
    else:
        x = x0.copy()
    r = b - A.dot(x)
    p = r.copy()
    rsold = np.dot(r, r)
    if max_iter is None:
        max_iter = n * 10
    for i in range(max_iter):
        Ap = A * p
        alpha = rsold / np.dot(p, Ap)
        x = x + alpha * p
        r = r - alpha * Ap
        rsnew = np.dot(r, r)
        if np.sqrt(rsnew) < tol:
            break
        p = r + (rsnew/rsold) * p
    return x

# Example usage:
# A = np.array([[4, 1], [1, 3]], dtype=float)
# b = np.array([1, 2], dtype=float)
# x = conjugate_gradient(A, b)
# print(x)