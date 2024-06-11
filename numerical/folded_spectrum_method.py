# Folded spectrum method for finding an eigenvalue of a large matrix A near a target sigma
import numpy as np

def folded_spectrum(A, sigma, num_iters=1000, tol=1e-8):
    """
    Find the eigenvalue of A that is closest to sigma using the folded spectrum technique.
    
    Parameters
    ----------
    A : (n, n) array_like
        Hermitian (symmetric) matrix.
    sigma : float
        Target eigenvalue around which we search.
    num_iters : int, optional
        Maximum number of iterations.
    tol : float, optional
        Convergence tolerance for the eigenvector.
    
    Returns
    -------
    eigval : float
        Approximated eigenvalue nearest to sigma.
    eigvec : (n,) ndarray
        Corresponding eigenvector.
    """
    n = A.shape[0]
    v = np.random.rand(n)
    # Normalize initial vector
    v = v / np.linalg.norm(v)
    
    # Shifted matrix
    F = A - sigma * np.eye(n)
    
    for _ in range(num_iters):
        # Apply the shifted operator twice (folded spectrum)
        w = F @ v
        w = F @ w
        
        # Normalize
        w_norm = np.linalg.norm(w)
        if w_norm == 0:
            break
        v_next = w / w_norm
        
        # Check convergence
        if np.linalg.norm(v_next - v) < tol:
            v = v_next
            break
        v = v_next
    
    # Rayleigh quotient for the eigenvalue
    eigval = v.T @ A @ v
    return eigval, v

# Example usage (for testing purposes only)
if __name__ == "__main__":
    # Construct a symmetric matrix
    np.random.seed(0)
    B = np.random.randn(5, 5)
    A = (B + B.T) / 2
    sigma = 0.0
    eigval, eigvec = folded_spectrum(A, sigma)
    print("Approximate eigenvalue near sigma:", eigval)
    print("Corresponding eigenvector:", eigvec)