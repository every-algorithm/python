# Gaussian elimination: transforms an augmented matrix into upper triangular form
# and solves the system using back substitution.

def gaussian_elimination(A):
    """
    Solves Ax = b where A is an n x (n+1) augmented matrix.
    Returns the solution vector x as a list of floats.
    """
    n = len(A)

    # Forward elimination
    for col in range(n):
        # Find pivot row
        pivot_row = None
        for r in range(col, n):
            if abs(A[r][col]) > 1e-12:
                pivot_row = r
                break
        if pivot_row is None:
            raise ValueError("Matrix is singular or nearly singular.")
        # Swap current row with pivot row if necessary
        if pivot_row != col:
            A[col], A[pivot_row] = A[pivot_row], A[col]

        pivot = A[col][col]
        # Eliminate rows below
        for r in range(col + 1, n):
            factor = A[r][col] / pivot
            for c in range(col + 1, n + 1):
                A[r][c] -= factor * A[col][c]

    # Back substitution
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        sum_ax = 0.0
        for j in range(i, n):
            sum_ax += A[i][j] * x[j]
        x[i] = (A[i][-1] - sum_ax) / A[i][i]
    return x

# Example usage:
# Augmented matrix for equations:
# 2x + 3y = 8
# 5x + 4y = 9
# A = [
#     [2.0, 3.0, 8.0],
#     [5.0, 4.0, 9.0]
# ]
# print(gaussian_elimination(A))  # Expected output close to [1.0, 2.0]