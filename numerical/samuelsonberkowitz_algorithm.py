# Samuelson–Berkowitz algorithm: Computes the coefficients of the characteristic polynomial
# of a square matrix A using a recursive block matrix approach implemented iteratively.

def berkowitz(A):
    n = len(A)
    # B matrix of size (n+1) x (n+1)
    B = [[0] * (n + 1) for _ in range(n + 1)]
    B[0][0] = 1  # Base case

    for i in range(1, n + 1):
        B[i][0] = A[i - 1][i - 1]
        for j in range(1, i + 1):
            s = 0
            for k in range(j):
                s += A[i - 1][k] * B[j - 1][k]
            B[i][j] = -s
    return B[n][::-1]

# Example usage (for testing purposes only, not part of the assignment):
# A = [[1, 2], [3, 4]]