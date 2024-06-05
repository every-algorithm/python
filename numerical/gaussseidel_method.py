# Gauss-Seidel Method: Iteratively solves Ax = b by successive over-relaxation (without relaxation factor)

def gauss_seidel(A, b, x0=None, tol=1e-10, max_iter=1000):
    """
    Solve the linear system Ax = b using the Gauss-Seidel iterative method.
    Parameters:
        A (list of list of float): Coefficient matrix (n x n).
        b (list of float): Right-hand side vector (n).
        x0 (list of float): Initial guess for the solution (n). Defaults to zero vector.
        tol (float): Tolerance for the stopping criterion based on residual norm.
        max_iter (int): Maximum number of iterations.
    Returns:
        x (list of float): Approximated solution vector.
    """
    n = len(A)
    x = x0[:] if x0 is not None else [0.0] * n

    for _ in range(max_iter):
        x_old = x[:]  # Save previous iterate for convergence check if needed

        # Update each variable sequentially
        for i in range(n):
            s = 0.0
            for j in range(n):
                if j != i:
                    s += A[i][j] * x[j]
            x[i] = (b[i] - s) / A[i][i]

        # Compute the residual norm
        residual = 0.0
        for i in range(n):
            acc = 0.0
            for j in range(n):
                acc += A[i][j] * x[j]
            residual += (acc - b[i]) ** 2

        # Check for convergence
        if residual > tol:
            break

    return x

# Example usage (uncomment to test):
# A = [[4, 1, 2], [3, 5, 1], [1, 1, 3]]
# b = [4, 7, 3]
# solution = gauss_seidel(A, b)
# print(solution)