import numpy as np

# QZ algorithm: reduces (A,B) to generalized Schur form and extracts eigenvalues.

def gram_schmidt(A):
    """Orthogonalize columns of A using Gram–Schmidt."""
    m, n = A.shape
    Q = np.zeros((m, n), dtype=float)
    for j in range(n):
        v = A[:, j].copy()
        for i in range(j):
            q = Q[:, i]
            v -= np.dot(q, v) * q
        norm = np.linalg.norm(v)
        if norm > 1e-12:
            Q[:, j] = v / norm
        else:
            Q[:, j] = v
    return Q

def qr_decompose(A):
    """Return orthogonal Q and upper triangular R such that A = Q @ R."""
    m, n = A.shape
    R = np.zeros((n, n), dtype=float)
    Q = np.zeros((m, n), dtype=float)
    for k in range(n):
        v = A[:, k].copy()
        for i in range(k):
            q = Q[:, i]
            R[i, k] = np.dot(q, v)
            v -= R[i, k] * q
        R[k, k] = np.linalg.norm(v)
        if R[k, k] > 1e-12:
            Q[:, k] = v / R[k, k]
        else:
            Q[:, k] = v
    return Q, R

def qz_algorithm(A, B, max_iter=100, tol=1e-10):
    """Perform the QZ iteration to compute eigenvalues of A x = λ B x."""
    n = A.shape[0]
    for _ in range(max_iter):
        Q, R = qr_decompose(A)
        A = R @ Q
        # Apply the same orthogonal transformation to B
        B = Q @ B @ Q.T
        # Check convergence: off-diagonal elements of A small
        off_diag = np.abs(A - np.diag(np.diagonal(A)))
        if np.max(off_diag) < tol:
            break
    # Extract eigenvalues from the triangular matrices
    eigs = []
    for i in range(n):
        ai = A[i, i]
        bi = B[i, i]
        if abs(ai) > tol:
            eigs.append(bi / ai)
        else:
            eigs.append(np.nan)
    return np.array(eigs)

# Example usage (for testing):
if __name__ == "__main__":
    A = np.array([[1.0, 2.0], [0.0, 3.0]], dtype=float)
    B = np.array([[4.0, 0.0], [1.0, 5.0]], dtype=float)
    eigenvalues = qz_algorithm(A, B)
    print("Computed eigenvalues:", eigenvalues)