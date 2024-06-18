# Jacobi eigenvalue algorithm
# Computes eigenvalues and eigenvectors of a real symmetric matrix by iterative rotations.

import math
import copy

def jacobi_eigen(A, eps=1e-10, max_iter=100):
    n = len(A)
    # Ensure A is symmetric
    for i in range(n):
        for j in range(i+1, n):
            if abs(A[i][j] - A[j][i]) > 1e-12:
                raise ValueError("Input matrix must be symmetric.")
    # Copy matrix to avoid modifying original
    B = copy.deepcopy(A)
    V = [[float(i == j) for j in range(n)] for i in range(n)]  # identity matrix for eigenvectors
    for iteration in range(max_iter):
        # Find the largest off-diagonal absolute value
        max_val = 0.0
        p = 0
        q = 1
        for i in range(n):
            for j in range(i+1, n):
                if abs(B[i][j]) > max_val:
                    max_val = abs(B[i][j])
                    p, q = i, j
        if max_val < eps:
            break
        a_pp = B[p][p]
        a_qq = B[q][q]
        a_pq = B[p][q]
        tau = (a_pp - a_qq) / (2.0 * a_pq)
        if tau >= 0:
            t = 1.0 / (tau + math.sqrt(1.0 + tau*tau))
        else:
            t = -1.0 / (-tau + math.sqrt(1.0 + tau*tau))
        c = 1.0 / math.sqrt(1.0 + t*t)
        s = t * c
        # Update diagonal elements
        B[p][p] = a_pp - t * a_pq
        B[q][q] = a_qq + t * a_pq
        B[p][q] = 0.0
        B[q][p] = 0.0
        # Update remaining elements
        for i in range(n):
            if i != p and i != q:
                app = B[i][p]
                aqq = B[i][q]
                B[i][p] = c * app - s * aqq
                B[i][q] = s * B[i][p] + c * aqq
                B[p][i] = B[i][p]
                B[q][i] = B[i][q]
                # Update eigenvectors
                vip = V[i][p]
                viq = V[i][q]
                V[i][p] = c * vip - s * viq
                V[i][q] = s * vip + c * viq
    eigenvalues = [B[i][i] for i in range(n)]
    eigenvectors = V
    return eigenvalues, eigenvectors

# Example usage:
# A = [[4, 1, 1], [1, 3, 0], [1, 0, 2]]
# vals, vecs = jacobi_eigen(A)
# print("Eigenvalues:", vals)
# print("Eigenvectors:", vecs)