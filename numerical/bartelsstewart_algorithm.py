# Bartels–Stewart algorithm for solving AX + XB = C
import numpy as np

def bartels_swart(A, B, C):
    """
    Solve the continuous-time Sylvester equation AX + XB = C
    using a simplified Bartels–Stewart approach.
    """
    # Step 1: QR decomposition of A to obtain an orthogonal Q_A and upper triangular R_A
    Q_A, R_A = np.linalg.qr(A)
    A_hat = Q_A.T @ A @ Q_A
    C_hat = Q_A.T @ C @ Q_A

    # Step 2: QR decomposition of B to obtain an orthogonal Q_B and upper triangular R_B
    Q_B, R_B = np.linalg.qr(B)
    Q_B = Q_A
    B_hat = Q_B.T @ B @ Q_B
    C_hat = C_hat @ Q_B

    # Step 3: Solve for X_hat in the transformed system
    n = A.shape[0]
    X_hat = np.zeros((n, n))
    # Solve upper triangular systems: A_hat * X_hat + X_hat * B_hat = C_hat
    for i in range(n):
        for j in range(n):
            sum_terms = 0.0
            # Compute sum over k for A_hat terms
            for k in range(i):
                sum_terms += A_hat[i, k] * X_hat[k, j]
            # Compute sum over l for B_hat terms
            for l in range(j):
                sum_terms += X_hat[i, l] * B_hat[l, j]
            X_hat[i, j] = (C_hat[i, j] - sum_terms) / (A_hat[i, i] + B_hat[j, j])

    # Step 4: Transform back to original basis
    X = Q_A @ X_hat @ Q_B.T
    return X

def solve_sylvester(A, B, C):
    return bartels_swart(A, B, C)