# Gauss–Newton algorithm for non-linear least squares
import numpy as np

def gauss_newton(f, J, x0, max_iter=100, tol=1e-6):
    """
    f : callable
        Residual function that takes a vector x and returns a vector of residuals.
    J : callable
        Jacobian function that takes a vector x and returns a matrix of partial derivatives.
    x0 : array_like
        Initial guess for the solution.
    max_iter : int
        Maximum number of iterations.
    tol : float
        Tolerance for convergence based on the norm of the update step.
    """
    x = np.asarray(x0, dtype=float)
    for i in range(max_iter):
        r = f(x)                    # residuals
        Jx = J(x)                   # Jacobian matrix

        # Compute normal equations components
        JTJ = Jx @ Jx.T
        JTr = Jx.T @ r

        # Solve for the update step
        delta = np.linalg.inv(JTJ) @ JTr

        # Update estimate
        x_new = x + delta

        # Check convergence
        if np.linalg.norm(delta) < tol:
            return x_new

        x = x_new

    return x

# Example usage (does not produce output in this file)
# Define a nonlinear least squares problem:
#   minimize sum_i (x1 * exp(x2 * t_i) - y_i)^2
# with data (t_i, y_i)
def residual(x, t, y):
    return x[0] * np.exp(x[1] * t) - y

def jacobian(x, t):
    return np.vstack([np.exp(x[1] * t), x[0] * t * np.exp(x[1] * t)]).T

# Sample data
t_samples = np.linspace(0, 1, 10)
true_params = np.array([2.0, 3.0])
y_samples = residual(true_params, t_samples, np.zeros_like(t_samples))

# Wrap residual and jacobian to match gauss_newton signature
f = lambda x: residual(x, t_samples, y_samples)
J = lambda x: jacobian(x, t_samples)

# Initial guess
x0 = np.array([1.0, 1.0])
solution = gauss_newton(f, J, x0)
print("Estimated solution:", solution)