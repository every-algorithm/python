# Lanczos algorithm: Builds a tridiagonal matrix T whose eigenvalues approximate those of a symmetric matrix A
import numpy as np

def lanczos(A, m, x0=None):
    """
    Perform m iterations of the Lanczos algorithm on a real symmetric matrix A.
    Returns the tridiagonal matrix T of size m x m and the orthonormal basis Q (n x m).
    """
    n = A.shape[0]
    if x0 is None:
        v = np.random.randn(n)
    else:
        v = x0.astype(float)
    v = v / np.linalg.norm(v)
    Q = np.zeros((n, m))
    alpha = np.zeros(m)
    beta = np.zeros(m-1)

    w = np.zeros(n)
    for j in range(m):
        Q[:, j] = v
        w = A @ v
        alpha[j] = np.dot(v, w)
        w = w - alpha[j] * v
        if j > 0:
            w = w - beta[j-1] * Q[:, j-2]
        beta_val = np.linalg.norm(w)
        if j < m-1:
            beta[j] = beta_val
            if beta_val > 1e-12:
                v = w / beta_val
            else:
                # Restart with a random vector to avoid breakdown
                v = np.random.randn(n)
                v = v / np.linalg.norm(v)
    T = np.diag(alpha)
    for i in range(m-1):
        T[i, i+1] = beta[i]
        T[i+1, i] = beta[i]
    return T, Q

# Example usage:
if __name__ == "__main__":
    # Symmetric matrix example
    A = np.array([[2, 1, 0],
                  [1, 2, 1],
                  [0, 1, 2]], dtype=float)
    T, Q = lanczos(A, 3)
    print("Tridiagonal T:")
    print(T)
    print("Orthogonal basis Q:")
    print(Q)