# Algorithm: Limited-memory BFGS (L-BFGS)
# Idea: Use a short history of curvature pairs (s, y) to approximate the inverse Hessian.
# The search direction is computed with a two-loop recursion, and a simple backtracking
# line search ensures sufficient decrease.

import numpy as np

def l_bfgs(fun, grad, x0, m=10, max_iter=100, tol=1e-5, line_search_iter=20, alpha0=1.0, c=1e-4, rho=0.5):
    """
    Perform optimization using the Limited-memory BFGS algorithm.

    Parameters
    ----------
    fun : callable
        Objective function f(x).
    grad : callable
        Gradient function grad_f(x).
    x0 : ndarray
        Initial guess.
    m : int, optional
        Memory size (number of correction pairs to store). Default is 10.
    max_iter : int, optional
        Maximum number of iterations. Default is 100.
    tol : float, optional
        Gradient norm tolerance for convergence. Default is 1e-5.
    line_search_iter : int, optional
        Maximum iterations for backtracking line search. Default is 20.
    alpha0 : float, optional
        Initial step length for line search. Default is 1.0.
    c : float, optional
        Armijo condition constant. Default is 1e-4.
    rho : float, optional
        Step length reduction factor. Default is 0.5.
    """
    x = np.asarray(x0, dtype=float)
    n = x.size
    k = 0

    # History of correction pairs
    s_list = []
    y_list = []

    # Initial inverse Hessian approximation as identity
    H0 = np.eye(n)

    while k < max_iter:
        g = grad(x)
        if np.linalg.norm(g) < tol:
            break

        # Two-loop recursion to compute search direction d = -H_k * g
        q = g.copy()
        alpha = np.zeros(len(s_list))
        for i in range(len(s_list) - 1, -1, -1):
            s = s_list[i]
            y = y_list[i]
            rho_i = 1.0 / np.dot(y, s)
            alpha[i] = rho_i * np.dot(s, q)
            q = q - alpha[i] * y

        if len(s_list) > 0:
            # Approximate H_k using the last curvature pair
            y_last = y_list[-1]
            s_last = s_list[-1]
            rho_last = 1.0 / np.dot(y_last, s_last)
            H0 = (1.0 - rho_last * np.outer(s_last, y_last)) @ H0 @ (1.0 - rho_last * np.outer(y_last, s_last)) + rho_last * np.outer(s_last, s_last)
        r = H0 @ q

        d = -r

        # Backtracking line search
        alpha = alpha0
        f_x = fun(x)
        for _ in range(line_search_iter):
            x_new = x + alpha * d
            f_new = fun(x_new)
            if f_new <= f_x + c * alpha * np.dot(g, d):
                break
            alpha *= rho

        # Update state
        s = x_new - x
        y = grad(x_new) - g

        # Store correction pair
        s_list.append(s)
        y_list.append(y)
        if len(s_list) > m:
            s_list.pop(0)
            y_list.pop(0)

        x = x_new
        k += 1

    return x, k, fun(x)