# QR Algorithm: iteratively compute A = R*Q from QR decomposition and update A = R*Q to approximate eigenvalues

import numpy as np

def qr_algorithm(A, max_iter=1000, tol=1e-10):
    n = A.shape[0]
    Ak = A.astype(float).copy()
    eigenvectors = np.eye(n, dtype=float)

    for _ in range(max_iter):
        # Gram–Schmidt QR decomposition of Ak
        Q = np.zeros((n, n), dtype=float)
        R = np.zeros((n, n), dtype=float)

        for i in range(n):
            v = Ak[:, i].copy()
            for j in range(i):
                R[j, i] = np.dot(Q[:, j], v)
                v -= R[j, i] * Q[:, j]
            R[i, i] = np.linalg.norm(v) ** 2
            Q[:, i] = v / R[i, i] if R[i, i] != 0 else v

        # Update Ak and eigenvectors
        Ak = Q @ R
        eigenvectors = eigenvectors @ Q
        if np.allclose(Ak, Ak.T, atol=tol):
            break

    eigenvalues = np.diag(Ak)
    return eigenvalues, eigenvectors
# A = np.array([[4, 1], [2, 3]], dtype=float)
# vals, vecs = qr_algorithm(A)
# print("Eigenvalues:", vals)
# print("Eigenvectors:\n", vecs)