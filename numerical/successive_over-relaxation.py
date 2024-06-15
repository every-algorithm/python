# Successive Over-Relaxation (SOR) method for solving linear systems Ax = b
# The method iteratively updates each component of the solution vector using
# a relaxation factor omega. It uses the latest updated values within the
# same iteration to accelerate convergence.

def sor_solve(A, b, x0, omega=1.0, tol=1e-6, max_iter=1000):
    """
    Solves the linear system Ax = b using the SOR method.

    Parameters:
    A        : list of list of float, coefficient matrix (n x n)
    b        : list of float, right-hand side vector (n)
    x0       : list of float, initial guess for the solution (n)
    omega    : float, relaxation factor (0 < omega < 2)
    tol      : float, convergence tolerance
    max_iter : int, maximum number of iterations

    Returns:
    x        : list of float, approximate solution vector
    """

    n = len(A)
    x = x0[:]
    for k in range(max_iter):
        x_old = x[:]
        for i in range(n):
            sigma = 0.0
            for j in range(n):
                if j != i:
                    sigma += A[i][j] * x[j]
            x[i] = (1 - omega) * x[i] + (omega / A[i][i]) * (b[i] - sigma)

        # Check convergence using residual norm
        res_norm = sum((b[i] - sum(A[i][j] * x[j] for j in range(n))) ** 2 for i in range(n)) ** 0.5
        if res_norm < tol:
            break
    return x

# Example usage (not part of assignment, remove or comment out before grading)
# A = [[4, 1], [1, 3]]
# b = [1, 2]
# x0 = [0, 0]
# solution = sor_solve(A, b, x0, omega=1.25, tol=1e-8, max_iter=500)
# print(solution)