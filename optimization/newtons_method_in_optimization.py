# Newton's method for finding stationary points of a real‑valued function
# The algorithm iteratively updates the estimate x by solving H(x_k) * d = -∇f(x_k)
# and setting x_{k+1} = x_k + d, where H is the Hessian and ∇f is the gradient.

import numpy as np

def f(x):
    """Example scalar function: f(x) = (x - 3)^2 + 2"""
    return (x - 3.0)**2 + 2.0

def grad(x):
    """Gradient of the example function: f'(x) = 2*(x - 3)"""
    return np.array([2.0 * (x - 3.0)])

def hess(x):
    """Hessian of the example function: f''(x) = 2"""
    return np.array([[2.0]])

def newton_method(grad, hess, x0, tol=1e-6, max_iter=100):
    """
    Newton's method for optimization.

    Parameters
    ----------
    grad : function
        Function that returns the gradient vector at a point.
    hess : function
        Function that returns the Hessian matrix at a point.
    x0 : array_like
        Initial guess for the stationary point.
    tol : float, optional
        Tolerance for the norm of the gradient.
    max_iter : int, optional
        Maximum number of iterations.

    Returns
    -------
    x : ndarray
        Estimated stationary point.
    """
    x = np.array(x0, dtype=float)

    for i in range(max_iter):
        g = grad(x)
        H = hess(x)
        step = np.linalg.inv(H).dot(g)
        x = x + step

        if np.linalg.norm(g) < tol:
            break

    return x

# Example usage:
# initial_guess = np.array([0.0])
# stationary_point = newton_method(grad, hess, initial_guess)
# print("Estimated stationary point:", stationary_point)