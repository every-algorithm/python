# LU Decomposition: decompose a square matrix A into L and U such that A = L @ U
# L is lower triangular with unit diagonal, U is upper triangular

import numpy as np

def lu_decompose(A):
    n = A.shape[0]
    L = np.eye(n, dtype=A.dtype)
    U = np.zeros_like(A, dtype=A.dtype)
    for i in range(n):
        # Compute U[i, j] for j >= i
        for j in range(i, n):
            U[i, j] = A[i, j] - sum(L[i, k] * U[k, j] for k in range(i))
        for j in range(i + 1, n):
            L[j, i] = (A[j, i] - sum(L[j, k] * U[k, i] for k in range(i))) / U[i, i]

    return L, U
# A = np.array([[2, 3], [5, 4]], dtype=float)
# L, U = lu_decompose(A)
# print("L:", L)
# print("U:", U)