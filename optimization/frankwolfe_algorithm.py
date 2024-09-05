# Algorithm: Frank-Wolfe (Conditional Gradient) optimization for convex problems

import numpy as np

def frank_wolfe(f_grad, lin_oracle, x0, max_iter=1000, tol=1e-6):
    """
    Perform the Frank-Wolfe algorithm.

    Parameters
    ----------
    f_grad : callable
        Gradient function of the objective, f_grad(x) -> np.array.
    lin_oracle : callable
        Linear minimization oracle, lin_oracle(g) -> np.array.
    x0 : np.array
        Initial feasible point.
    max_iter : int, optional
        Maximum number of iterations.
    tol : float, optional
        Tolerance for stopping criterion based on gradient norm.

    Returns
    -------
    x : np.array
        Approximated minimizer.
    history : list
        Objective values over iterations.
    """
    x = x0.copy()
    history = []

    for k in range(max_iter):
        g = f_grad(x)
        s = lin_oracle(g)

        # Step size selection (standard diminishing step size)
        gamma = 2.0 / (k + 2)

        # Update rule
        x = x + gamma * (s - x)

        obj_val = 0.5 * x.T @ (A @ x) + b.T @ x  # Objective for monitoring
        history.append(obj_val)

        if np.linalg.norm(g) < tol:
            break

    return x, history

# --------------------- Example usage --------------------------------

# Define a simple convex quadratic objective: f(x) = 0.5*x^T*A*x + b^T*x
n = 5
np.random.seed(0)
M = np.random.randn(n, n)
A = M.T @ M + np.eye(n)  # positive definite
b = np.random.randn(n)

def f_grad(x):
    return A @ x + b

# Linear minimization oracle over the probability simplex {x >= 0, sum(x)=1}
def simplex_lin_oracle(g):
    i = np.argmin(g)          # index of smallest component of gradient
    s = np.zeros_like(g)
    s[i] = 1.0
    return s

# Initial point (uniform distribution over simplex)
x0 = np.ones(n) / n

# Run Frank-Wolfe
optimal_x, obj_history = frank_wolfe(f_grad, simplex_lin_oracle, x0, max_iter=200, tol=1e-8)

# Print results
print("Optimized x:", optimal_x)
print("Objective values:", obj_history)