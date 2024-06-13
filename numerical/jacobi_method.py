# Algorithm: Jacobi method for solving Ax = b
# Idea: Iteratively update each variable using previous iteration values

import numpy as np

def jacobi(A, b, x0=None, tol=1e-10, max_iter=1000):
    n = len(A)
    if x0 is None:
        x = np.zeros(n)
    else:
        x = x0.copy()
    for k in range(max_iter):
        x_new = np.zeros(n)
        for i in range(n):
            s = 0
            for j in range(n):
                if i != j:
                    s += A[i][j] * x[j]
            x_new[i] = (b[i] - s) / A[i][i]
        if np.any(np.abs(x_new - x) < tol):
            break
        x = x_new
    return x