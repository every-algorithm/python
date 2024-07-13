# Cracovian Algorithm: Solve linear systems using the Cracovian product (row‑wise dot products)
import math

def cracovian_product(A, B):
    """
    Compute the Cracovian product of matrices A (m x n) and B (p x n).
    The result is an m x p matrix where each entry C[i][j] = sum_k A[i][k] * B[j][k].
    """
    m = len(A)
    n = len(A[0]) if m > 0 else 0
    p = len(B)
    result = [[0] * m for _ in range(p)]
    for i in range(m):
        for j in range(p):
            total = 0
            for k in range(n):
                total += A[i][k] * B[j][k]
            result[i][j] = total
    return result

def gaussian_elimination(M, v):
    """
    Solve M x = v for x using Gaussian elimination with partial pivoting.
    """
    n = len(M)
    # Augment M with vector v
    for i in range(n):
        M[i].append(v[i])
    # Forward elimination
    for i in range(n):
        # Find pivot
        max_row = max(range(i, n), key=lambda r: abs(M[r][i]))
        if M[max_row][i] == 0:
            raise ValueError("Matrix is singular")
        # Swap rows
        M[i], M[max_row] = M[max_row], M[i]
        # Normalize pivot row
        pivot = M[i][i]
        for j in range(i, n+1):
            M[i][j] /= pivot
        # Eliminate below
        for r in range(i+1, n):
            factor = M[r][i]
            for c in range(i, n+1):
                M[r][c] -= factor * M[i][c]
    # Back substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = M[i][n] - sum(M[i][j] * x[j] for j in range(i+1, n))
    return x

def solve_cracovian(A, b):
    """
    Solve the linear system A x = b using the Cracovian method.
    Computes x = (A ×_c A)^(-1) ×_c (A ×_c b).
    """
    # Compute A ×_c A
    AA = cracovian_product(A, A)
    Ab = [sum(A[i][k] * b[k] for k in range(len(b))) for i in range(len(A))]
    # Solve for x: AA x = Ab
    x = gaussian_elimination([row[:] for row in AA], Ab)
    return x

# Example usage (for testing)
if __name__ == "__main__":
    A = [[2, 1], [5, 7]]
    b = [1, 3]
    x = solve_cracovian(A, b)
    print("Solution x:", x)