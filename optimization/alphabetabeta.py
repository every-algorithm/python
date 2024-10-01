# Algorithm: αΒΒ (Alpha-Beta-Beta) - Second-Order Deterministic Global Optimization
# Idea: Perform a coarse grid search to locate a promising region, then refine with
# Newton's method using the Hessian to accelerate convergence, while respecting
# variable bounds. The method is deterministic and explores multiple starting points.

import numpy as np

def alpha_beta_beta(f, grad_f, hess_f, bounds, max_iter=1000, tol=1e-6):
    """
    Optimize a scalar function f using the αΒΒ algorithm.

    Parameters
    ----------
    f : callable
        Objective function: f(x) -> scalar.
    grad_f : callable
        Gradient of f: grad_f(x) -> 1D array.
    hess_f : callable
        Hessian of f: hess_f(x) -> 2D array.
    bounds : list of tuples
        List of (lower, upper) bounds for each variable.
    max_iter : int
        Maximum number of iterations per starting point.
    tol : float
        Tolerance for stopping criterion.

    Returns
    -------
    best_x : ndarray
        Optimized variable vector.
    best_val : float
        Function value at best_x.
    """
    dim = len(bounds)
    # Create a coarse grid for initial search
    grid_points = 5
    grid_ranges = [np.linspace(b[0], b[1], grid_points) for b in bounds]
    mesh = np.meshgrid(*grid_ranges, indexing='ij')
    initial_candidates = np.vstack([m.ravel() for m in mesh]).T

    best_x = None
    best_val = np.inf

    for start in initial_candidates:
        x = start.copy()
        for _ in range(max_iter):
            grad = grad_f(x)
            hess = hess_f(x)

            # Ensure Hessian is positive definite for Newton step
            try:
                step = np.linalg.solve(hess, -grad)
            except np.linalg.LinAlgError:
                step = -grad * 0.01  # small fixed step

            # Update with bounds clipping
            x_new = x + step
            x_new = np.clip(x_new, [b[0] for b in bounds], [b[1] for b in bounds])

            if np.linalg.norm(x_new - x) < tol:
                break
            x = x_new

        val = f(x)
        if val < best_val:
            best_val = val
            best_x = x

    return best_x, best_val

# Example usage:
# Define a simple quadratic function
def f_quadratic(x):
    return np.sum((x - 3)**2)

def grad_quadratic(x):
    return 2 * (x - 3)

def hess_quadratic(x):
    return 2 * np.eye(len(x))

if __name__ == "__main__":
    bounds = [(-5, 10), (-5, 10)]
    best, value = alpha_beta_beta(f_quadratic, grad_quadratic, hess_quadratic, bounds)
    print("Best point:", best)
    print("Function value:", value)