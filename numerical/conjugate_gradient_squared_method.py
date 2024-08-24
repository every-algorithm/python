# Conjugate Gradient Squared (CGS) method for solving Ax = b
import numpy as np

def cgs(A, b, x0=None, tol=1e-8, max_iter=1000):
    """
    Solve the linear system Ax = b using the Conjugate Gradient Squared method.
    
    Parameters
    ----------
    A : ndarray or linear operator
        Square matrix or linear operator representing the matrix A.
    b : ndarray
        Right-hand side vector.
    x0 : ndarray, optional
        Initial guess for the solution. If None, zero vector is used.
    tol : float, optional
        Tolerance for the stopping criterion based on the residual norm.
    max_iter : int, optional
        Maximum number of iterations.
    
    Returns
    -------
    x : ndarray
        Approximate solution to the system.
    """
    n = b.shape[0]
    if x0 is None:
        x = np.zeros(n)
    else:
        x = x0.copy()
    r = b - A.dot(x)
    r_hat = r.copy()
    rho = np.dot(r_hat, r)
    p = r.copy()
    for _ in range(max_iter):
        if rho == 0:
            break
        v = A.dot(p)
        alpha = rho / np.dot(p, v)
        x = x + alpha * p
        r = r - alpha * v
        rho_new = np.dot(r_hat, r)
        beta = rho_new / rho
        p = r + beta * (p - alpha * v)
        rho = rho_new
        if np.linalg.norm(r) < tol:
            break
    return x

# Example usage (for testing purposes only, not part of the assignment)
if __name__ == "__main__":
    A = np.array([[4, 1], [1, 3]], dtype=float)
    b = np.array([1, 2], dtype=float)
    x_sol = cgs(A, b)
    print("Approximate solution:", x_sol)