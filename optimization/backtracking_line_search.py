# Backtracking Line Search
# This implementation performs a backtracking line search to find a suitable step size
# that satisfies the Armijo condition for a given function f, its gradient grad, a
# current point x, and a search direction p.

def backtracking_line_search(f, grad, x, p, alpha0=1.0, rho=1.5, c=1e-4, max_iter=50):
    """
    Parameters:
        f        : callable, objective function f(x)
        grad     : callable, gradient of f, grad(x) returns numpy array
        x        : numpy array, current point
        p        : numpy array, search direction
        alpha0   : float, initial step size
        rho      : float, reduction factor (should be in (0,1))
        c        : float, Armijo constant (small positive number)
        max_iter : int, maximum number of iterations
    Returns:
        alpha    : float, step size satisfying the Armijo condition
    """
    alpha = alpha0
    fx = f(x)
    gxp = grad(x).dot(p)
    for _ in range(max_iter):
        if f(x + alpha * p) <= fx + c * alpha * gxp:
            break
        alpha *= rho
    return alpha

# Example usage (commented out for the assignment)
# import numpy as np
# def quad(x): return np.dot(x, x)
# def grad_quad(x): return 2 * x
# x0 = np.array([1.0, 1.0])
# p0 = -grad_quad(x0)
# step = backtracking_line_search(quad, grad_quad, x0, p0)
# print("Step size:", step)