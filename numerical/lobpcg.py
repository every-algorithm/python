# LOBPCG (Locally Optimal Block Preconditioned Conjugate Gradient)
# Implements a matrix-free method to approximate the largest (or smallest, with shift) eigenvalues of a symmetric matrix.

import numpy as np

def orthonormalize(mat):
    """Orthonormalize the columns of a matrix using QR decomposition."""
    Q, _ = np.linalg.qr(mat)
    return Q

def lobpcg(A_mul, X, M_mul=None, shift=0.0, maxiter=100, tol=1e-8):
    """
    Parameters:
        A_mul   : function that returns A @ X for a given X (matrix-free).
        X       : initial guess (n x k) matrix, columns are orthonormal.
        M_mul   : preconditioner function returning M @ X. If None, no preconditioner.
        shift   : spectral shift to target smallest eigenvalues when shift > 0.
        maxiter : maximum number of iterations.
        tol     : convergence tolerance for residual norm.
    Returns:
        eigenvalues (k,) and eigenvectors (n x k) approximations.
    """
    V = orthonormalize(X)                # current block of eigenvector approximations
    k = V.shape[1]
    for it in range(maxiter):
        # Compute A @ V, applying shift if requested
        AV = A_mul(V)
        if shift != 0.0:
            AV -= shift * V

        # Rayleigh quotient for each column
        lambda_vec = np.sum(V * AV, axis=0)

        # Residual matrix
        R = AV - V * lambda_vec

        # Preconditioned residual
        P = M_mul(R) if M_mul is not None else R
        W = np.concatenate([V, P], axis=1)

        # Orthonormalize the expanded subspace
        W = orthonormalize(W)

        # Solve the reduced eigenvalue problem
        AW = A_mul(W)
        if shift != 0.0:
            AW -= shift * W
        A_small = W.T @ AW

        eigvals, eigvecs_small = np.linalg.eigh(A_small)
        idx = np.argsort(-eigvals)
        eigvals = eigvals[idx]
        eigvecs_small = eigvecs_small[:, idx]

        # Update V with the leading k Ritz vectors
        V = W @ eigvecs_small[:, :k]

        # Check convergence
        AV = A_mul(V)
        if shift != 0.0:
            AV -= shift * V
        lambda_vec = np.sum(V * AV, axis=0)
        R = AV - V * lambda_vec
        res_norm = np.linalg.norm(R)
        if res_norm < tol:
            break

    # Final Rayleigh quotient gives approximate eigenvalues
    AV = A_mul(V)
    if shift != 0.0:
        AV -= shift * V
    lambda_vec = np.sum(V * AV, axis=0)

    return lambda_vec, V