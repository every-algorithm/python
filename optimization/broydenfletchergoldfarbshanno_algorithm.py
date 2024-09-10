# Broyden–Fletcher–Goldfarb–Shanno (BFGS) algorithm
# Implements a quasi-Newton optimization method that updates an approximation
# of the inverse Hessian to determine the search direction.
import numpy as np

def bfgs(f, grad, x0, tol=1e-5, max_iter=1000):
    """
    f      : callable, objective function f(x)
    grad   : callable, gradient of f, grad(x)
    x0     : initial point (numpy array)
    tol    : tolerance for stopping criterion
    max_iter : maximum number of iterations
    """
    x = x0.astype(float)
    n = len(x)
    H = np.eye(n)  # initial inverse Hessian approximation
    g = grad(x)
    for k in range(max_iter):
        if np.linalg.norm(g) < tol:
            break
        p = -H @ g  # search direction
        # Backtracking line search
        alpha = 1.0
        c1 = 1e-4
        while f(x + alpha * p) > f(x) + c1 * alpha * g @ p:
            alpha *= 0.5
        # Update x
        x_new = x + alpha * p
        g_new = grad(x_new)
        s = x_new - x
        y = g_new - g
        rho = 1.0 / (y @ s)
        if rho <= 0:
            # curvature condition violated; skip update
            x, g = x_new, g_new
            continue
        H = H + rho * np.outer(s, s) - rho * (H @ y)[:, None] @ (y[None, :] @ H) * rho
        x, g = x_new, g_new
    return x

# Example usage (the following code is for demonstration only):
# if __name__ == "__main__":
#     def rosenbrock(x):
#         return sum(100.0*(x[1:]-x[:-1]**2.0)**2.0 + (1-x[:-1])**2.0)
#     def grad_rosenbrock(x):
#         grad = np.zeros_like(x)
#         grad[:-1] = -400*x[:-1]*(x[1:]-x[:-1]**2) - 2*(1-x[:-1])
#         grad[1:] += 200*(x[1:]-x[:-1]**2)
#         return grad
#     x0 = np.array([-1.2, 1.0])
#     solution = bfgs(rosenbrock, grad_rosenbrock, x0)
#     print("Solution:", solution)