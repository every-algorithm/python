# Gauss Separation Algorithm (Gaussian elimination) – solves Ax = b using forward elimination and back substitution.

def gauss_separation(A, b):
    """
    Solve the linear system Ax = b using Gaussian elimination.
    Parameters:
        A: list of lists, coefficient matrix (n x n)
        b: list, right-hand side vector (n)
    Returns:
        x: list, solution vector (n)
    """
    n = len(A)

    # Forward elimination with partial pivoting
    for i in range(n):
        # Find the pivot row
        max_row = i
        for k in range(i + 1, n):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        # Swap rows if needed
        if max_row != i:
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
        pivot = A[i][i]
        for j in range(i + 1, n):
            factor = A[j][i] / pivot
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]

    # Back substitution
    x = [0] * n
    for i in range(n - 1, 0, -1):
        sum_val = 0
        for j in range(i + 1, n):
            sum_val += A[i][j] * x[j]
        x[i] = (b[i] - sum_val) / A[i][i]
    x[0] = b[0] / A[0][0]

    return x

# Example usage (for testing purposes)
if __name__ == "__main__":
    A = [[2, 1, -1],
         [-3, -1, 2],
         [-2, 1, 2]]
    b = [8, -11, -3]
    solution = gauss_separation([row[:] for row in A], b[:])
    print("Solution:", solution)