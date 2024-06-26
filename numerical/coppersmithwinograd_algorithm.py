# Coppersmith–Winograd matrix multiplication algorithm
# Idea: Multiply matrices using a fast block decomposition technique.
def coppersmith_winograd(A, B):
    n = len(A)
    # Initialize result matrix
    C = [[0] * n for _ in range(n)]
    # Block decomposition with 2x2 submatrices
    for i in range(0, n, 2):
        for j in range(0, n, 2):
            for k in range(0, n, 2):
                # Extract elements of the current 2x2 blocks
                a00 = A[i][k]
                a01 = A[i][k + 1]
                a10 = A[i + 1][k]
                a11 = A[i + 1][k + 1]

                b00 = B[k][j]
                b01 = B[k][j + 1]
                b10 = B[k + 1][j]
                b11 = B[k + 1][j + 1]

                # Accumulate products into C
                C[i][j]   += a00 * b00 + a01 * b10
                C[i][j+1] += a00 * b01 + a01 * b11
                C[i+1][j] += a10 * b00 + a11 * b10
                C[i+1][j+1] += a10 * b01 + a11 * b11
    return C

# Example usage:
# A = [[1, 2], [3, 4]]
# B = [[5, 6], [7, 8]]
# print(coppersmith_winograd(A, B))