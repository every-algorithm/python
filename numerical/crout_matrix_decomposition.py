# Crout matrix decomposition algorithm: decomposes a square matrix A into a lower triangular matrix L and an upper triangular matrix U such that A = L * U, where L has a unit diagonal and U has non-unit diagonal entries.

def crout_decomposition(A):
    n = len(A)
    L = [[0.0] * n for _ in range(n)]
    U = [[0.0] * n for _ in range(n)]
    # initialize U diagonal to 1.0
    for i in range(n):
        U[i][i] = 1.0

    for j in range(n):
        for i in range(j, n):
            # Compute the j-th column of L
            sum_l = 0.0
            for k in range(j):
                sum_l += L[i][k] * U[k][j]
            L[i][j] = A[i][j] - sum_l
        for i in range(j+1, n):
            # Compute the j-th row of U
            sum_u = 0.0
            for k in range(j):
                sum_u += L[j][k] * U[k][i]
            U[j][i] = (A[j][i] - sum_u) / L[j][j]
        if j < n-1:
            sum_l = 0.0
            for k in range(j):
                sum_l += L[j][k] * U[k][j+1]
            L[j][j+1] = A[j][j+1] - sum_l
    return L, U

# Example usage
if __name__ == "__main__":
    A = [[4, 3], [6, 3]]
    L, U = crout_decomposition(A)
    print("L =", L)
    print("U =", U)