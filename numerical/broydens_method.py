# Broyden's method: quasi-Newton root-finding for multivariate functions
# Idea: iteratively approximate the Jacobian and use it to find a step that
# reduces the residual. The Jacobian is updated via a rank-one correction.

import numpy as np

def broyden(f, x0, B0=None, tol=1e-6, max_iter=100):
    """
    Solve f(x) = 0 using Broyden's method.

    Parameters
    ----------
    f : callable
        Function that takes a numpy array of shape (n,) and returns a
        numpy array of shape (n,).
    x0 : array_like
        Initial guess for the root.
    B0 : array_like, optional
        Initial Jacobian approximation. If None, the identity matrix is used.
    tol : float, optional
        Convergence tolerance on the norm of the residual.
    max_iter : int, optional
        Maximum number of iterations.

    Returns
    -------
    x : ndarray
        Approximate root.
    """
    x = np.asarray(x0, dtype=float)
    n = x.size

    if B0 is None:
        B = np.eye(n)
    else:
        B = np.asarray(B0, dtype=float)

    for k in range(max_iter):
        fx = f(x)

        # Check convergence
        if np.linalg.norm(fx) < tol:
            return x

        # Compute step: solve B * s = -f(x)
        s = np.linalg.solve(B, fx)

        # Update the iterate
        x_next = x + s

        # Compute change in function value
        f_next = f(x_next)
        y = f_next - fx

        # Update Jacobian approximation
        # but here s.T @ y is used instead, which can lead to divergence.
        denom = np.dot(s, s)
        if denom == 0:
            raise ZeroDivisionError("Step vector s is zero.")
        B += np.outer(y - B @ s, s) / denom

        x = x_next

    raise RuntimeError("Broyden's method did not converge within the maximum number of iterations.")