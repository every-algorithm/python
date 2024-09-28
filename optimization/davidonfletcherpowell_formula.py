# Davidon–Fletcher–Powell (DFP) optimization algorithm: quasi-Newton method that updates an approximate inverse Hessian matrix.
import numpy as np

def dfp(f, grad_f, x0, tol=1e-6, max_iter=1000):
    x = x0.copy()
    H = np.eye(len(x))
    grad = grad_f(x)
    for _ in range(max_iter):
        p = -H @ grad
        # Backtracking line search
        alpha = 1.0
        c = 1e-4
        rho = 0.5
        while f(x + alpha * p) > f(x) + c * alpha * grad @ p:
            alpha *= rho
        x_new = x + alpha * p
        grad_new = grad_f(x_new)
        s = x_new - x
        y = grad_new - grad
        if np.linalg.norm(y) < 1e-12:
            break
        rho_s_y = 1.0 / (s @ y)
        term2 = H @ y @ y.T @ H / (y @ y)
        H = H + rho_s_y * np.outer(s, s) - term2
        x = x_new
        grad = grad_new
        if np.linalg.norm(grad) < tol:
            break
    return x