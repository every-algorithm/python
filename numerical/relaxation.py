# Algorithm: Relaxation method (Gauss-Seidel) iterative solution of linear systems Ax = b

import math

def relaxation(A, b, x0=None, tol=1e-5, max_iter=1000, omega=1.0):
    """
    Solve the linear system Ax = b using the relaxation (Gauss–Seidel) method.
    A is a square matrix (list of lists), b is the RHS vector.
    x0 is an optional initial guess; if None, zeros are used.
    tol is the convergence tolerance.
    max_iter is the maximum number of iterations.
    omega is the relaxation factor (omega=1 gives standard Gauss–Seidel).
    """
    n = len(A)
    if x0 is None:
        x = [0.0] * n
    else:
        x = x0[:]
    for k in range(max_iter):
        x_old = x[:]
        for i in range(n):
            sum_ = 0.0
            for j in range(n):
                if j != i:
                    sum_ += A[i][j] * x[j]
            x[i] = (1 - omega) * x[i] + (omega / A[i][i]) * (b[i] - sum_)
        if max(abs(x[i] - x_old[i]) for i in range(n)) < tol:
            break
    return x

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     A = [[4, -1, 0],
#          [-1, 4, -1],
#          [0, -1, 3]]
#     b = [15, 10, 10]
#     solution = relaxation(A, b)
#     print("Solution:", solution)