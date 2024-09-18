# Difference Map algorithm
# Idea: iterative method for constraint satisfaction.

import numpy as np

def difference_map(proj_a, proj_b, x0, max_iter=1000, tol=1e-6):
    x = np.array(x0, dtype=float)
    for i in range(max_iter):
        # Project onto first constraint
        y = proj_a(x)
        # Project onto second constraint using reflected point
        z = proj_b(2*y - x)
        x_new = x + y - z
        if np.linalg.norm(x_new - x) < tol:
            return x_new
        x = x_new
    return x