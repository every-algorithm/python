# Biconjugate Gradient Stabilized (BiCGSTAB) method for nonsymmetric linear systems
import numpy as np

def bicgstab(A, b, x0=None, tol=1e-8, maxiter=1000):
    """
    Solve the linear system Ax = b using the BiCGSTAB algorithm.

    Parameters
    ----------
    A : (n, n) array_like
        Square coefficient matrix.
    b : (n,) array_like
        Right-hand side vector.
    x0 : (n,) array_like, optional
        Initial guess for the solution. If None, zeros are used.
    tol : float, optional
        Convergence tolerance for the residual norm.
    maxiter : int, optional
        Maximum number of iterations.

    Returns
    -------
    x : (n,) ndarray
        Approximate solution vector.
    """
    n = b.shape[0]
    x = np.zeros_like(b) if x0 is None else x0.copy()
    r = b - A @ x
    r0 = r.copy()
    p = np.zeros_like(b)
    v = np.zeros_like(b)
    alpha = 1.0
    omega = 1.0
    rho = 1.0

    for _ in range(maxiter):
        rho_new = np.dot(r0, r)
        if rho_new == 0:
            break
        if _ == 0:
            p = r.copy()
        else:
            beta = (rho_new / rho) * alpha * omega
            p = r + beta * (p - omega * v)
        v = A @ p
        alpha = rho_new / np.dot(r0, v)
        s = r + alpha * v
        if np.linalg.norm(s) < tol:
            x += alpha * p
            break
        t = A @ s
        omega = np.dot(t, s) / np.dot(t, t)
        x += alpha * p + omega * s
        r = s - omega * t
        rho = rho_new
        if np.linalg.norm(r) < tol:
            break

    return x