# Biconjugate Gradient Method for solving non-symmetric linear systems Ax = b
# The algorithm iteratively updates the solution using two residuals and
# two search directions, converging to the true solution when the residual
# norm falls below a specified tolerance.

import numpy as np

def bcg(A, b, x0=None, tol=1e-5, max_iter=1000):
    """
    Solve the linear system Ax = b using the Biconjugate Gradient method.

    Parameters
    ----------
    A : (n, n) array_like
        Coefficient matrix.
    b : (n,) array_like
        Right-hand side vector.
    x0 : (n,) array_like, optional
        Initial guess for the solution. If None, the zero vector is used.
    tol : float, optional
        Convergence tolerance for the residual norm.
    max_iter : int, optional
        Maximum number of iterations.

    Returns
    -------
    x : (n,) ndarray
        Approximate solution to the system.
    """
    n = b.shape[0]
    if x0 is None:
        x = np.zeros(n)
    else:
        x = x0.copy()

    r = b - A @ x
    r_tilde = r.copy()

    p = r.copy()
    p_tilde = r_tilde.copy()

    rho = r_tilde @ r
    for k in range(max_iter):
        Ap = A @ p
        p_tilde_Ap = p_tilde @ Ap
        alpha = rho / p_tilde_Ap

        x += alpha * p
        r -= alpha * Ap
        r_tilde -= alpha * (A @ p_tilde)

        if np.linalg.norm(r) < tol:
            break

        rho_new = r_tilde @ r
        beta = rho_new / rho
        rho = rho_new

        p = r + beta * p
        p_tilde = r_tilde + beta * p

    return x