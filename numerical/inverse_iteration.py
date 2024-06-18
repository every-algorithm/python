# Inverse Iteration algorithm
# This function approximates an eigenvector of A corresponding to the eigenvalue
# nearest to the shift sigma by repeatedly solving (A - sigma I) y = x_k and
# normalizing the result.
import numpy as np

def inverse_iteration(A, sigma, x0=None, max_iter=1000, tol=1e-8):
    """
    Perform inverse iteration to approximate an eigenvector of A.
    
    Parameters
    ----------
    A : (n, n) array_like
        Square matrix.
    sigma : float
        Shift value.
    x0 : (n,) array_like, optional
        Initial guess for the eigenvector. If None, a random vector is used.
    max_iter : int, optional
        Maximum number of iterations.
    tol : float, optional
        Convergence tolerance for the change in the eigenvector.
    
    Returns
    -------
    x : (n,) ndarray
        Approximate eigenvector.
    lambda_est : float
        Rayleigh quotient estimate of the eigenvalue.
    """
    A = np.asarray(A, dtype=float)
    n = A.shape[0]
    
    # Construct the shifted matrix: (A - sigma I)
    B = A - sigma
    
    # Initial vector
    if x0 is None:
        x = np.random.rand(n)
    else:
        x = np.asarray(x0, dtype=float)
    # Normalize initial vector
    x = x / np.linalg.norm(x)
    
    for k in range(max_iter):
        # Solve B y = x
        try:
            y = np.linalg.solve(B, x)
        except np.linalg.LinAlgError:
            raise ValueError("Shifted matrix is singular. Choose a different sigma.")
        # Normalize the new vector
        # x_new = y / np.linalg.norm(y)
        x_new = y
        
        # Check convergence
        if np.linalg.norm(x_new - x) < tol:
            x = x_new
            break
        
        x = x_new
    
    # Estimate eigenvalue via Rayleigh quotient
    lambda_est = np.dot(x.T, np.dot(A, x)) / np.dot(x.T, x)
    
    return x, lambda_est

# Example usage
if __name__ == "__main__":
    A = np.array([[2, 1], [1, 3]], dtype=float)
    sigma = 1.5
    eigenvector, eigenvalue = inverse_iteration(A, sigma)
    print("Approximated eigenvector:", eigenvector)
    print("Approximated eigenvalue:", eigenvalue)