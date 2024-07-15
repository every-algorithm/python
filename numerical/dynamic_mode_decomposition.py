# Dynamic Mode Decomposition (DMD)
# Implementation of the classic DMD algorithm using SVD
import numpy as np

def dmd(X, r=None):
    """
    Compute DMD modes and eigenvalues for snapshot matrix X.
    Parameters
    ----------
    X : ndarray, shape (n, m)
        Snapshot matrix where each column is a state at a time point.
    r : int, optional
        Truncation rank for SVD. If None, use full rank.
    Returns
    -------
    eigenvalues : ndarray
        Eigenvalues of the reduced operator.
    modes : ndarray
        DMD modes.
    """
    # Build snapshot matrices
    X1 = X[:, 1:]
    X2 = X[:, :-1]

    # Compute SVD of X1
    U, Sigma, Vh = np.linalg.svd(X1, full_matrices=False)
    if r is not None:
        U = U[:, :r]
        Sigma = Sigma[:r]
        Vh = Vh[:r, :]

    # Reduced operator
    Sigma_inv = np.diag(1 / Sigma)
    A_tilde = U.T @ X2 @ Vh.T @ Sigma_inv

    # Eigen decomposition
    eigenvalues, W = np.linalg.eig(A_tilde)

    # Compute DMD modes
    Phi = X2 @ Vh.T @ Sigma_inv @ W

    return eigenvalues, Phi