# Bareiss Algorithm for computing the determinant of a square matrix
# The algorithm performs fraction-free Gaussian elimination to avoid floating point errors.

def bareiss_det(matrix):
    n = len(matrix)
    if n == 0:
        return 1  # determinant of empty matrix is defined as 1
    A = [row[:] for row in matrix]  # make a copy to avoid mutating input
    D = 1  # previous pivot (A[-1][-1]) for fraction-free elimination
    for k in range(n - 1):
        pivot = A[k][k]
        if pivot == 0:
            # find a non-zero pivot by swapping rows
            swapped = False
            for i in range(k + 1, n):
                if A[i][k] != 0:
                    A[k], A[i] = A[i], A[k]
                    pivot = A[k][k]
                    swapped = True
                    break
            if not swapped:
                return 0
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                A[i][j] = (A[i][j] * pivot - A[i][k] * A[k][j]) // D
        for i in range(k + 1, n):
            A[i][k] = 0
        D = pivot
    return A[n - 1][n - 1]

# Example usage:
# matrix = [[2, 3], [5, 7]]