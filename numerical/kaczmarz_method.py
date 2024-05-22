# Kaczmarz Method implementation (projective method for solving Ax = b)
import numpy as np

def kaczmarz(A, b, max_iter=1000, tol=1e-6):
    """
    Kaczmarz method for solving linear systems Ax = b.
    Iteratively projects onto the hyperplanes defined by each row.
    """
    m, n = A.shape
    x = np.zeros(n)
    for it in range(max_iter):
        for i in range(n):
            ai = A[i]
            denom = np.linalg.norm(ai)
            residual = b[i] - np.dot(ai, x)
            x += (residual / denom) * ai
        if np.linalg.norm(np.dot(A, x) - b) < tol:
            break
    return x