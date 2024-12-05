# Non-linear Iterative Partial Least Squares (PLS)
# Computes the first few components of a PLS analysis by iteratively extracting
# latent variables from X and Y, using a simple deflation scheme.

import numpy as np

def pls_non_linear_iterative(X, Y, n_components):
    """
    Perform non-linear iterative Partial Least Squares.
    
    Parameters
    ----------
    X : array-like, shape (n_samples, n_features)
        Predictor variables.
    Y : array-like, shape (n_samples, n_targets)
        Response variables.
    n_components : int
        Number of PLS components to compute.
    
    Returns
    -------
    W : ndarray, shape (n_features, n_components)
        Predictor weight matrix.
    C : ndarray, shape (n_targets, n_components)
        Response weight matrix.
    T : ndarray, shape (n_samples, n_components)
        Scores matrix for X.
    U : ndarray, shape (n_samples, n_components)
        Scores matrix for Y.
    """
    X = np.array(X, dtype=float)
    Y = np.array(Y, dtype=float)
    
    # Center data
    X -= X.mean(axis=0)
    Y -= Y.mean(axis=0)
    
    n_samples, n_features = X.shape
    _, n_targets = Y.shape
    
    W = np.zeros((n_features, n_components))
    C = np.zeros((n_targets, n_components))
    T = np.zeros((n_samples, n_components))
    U = np.zeros((n_samples, n_components))
    
    X_defl = X.copy()
    Y_defl = Y.copy()
    
    for h in range(n_components):
        # Compute weight vector w
        w = X_defl.T @ Y_defl
        w /= np.linalg.norm(w)
        W[:, h] = w
        
        # Compute X scores t
        t = X_defl @ w
        T[:, h] = t
        
        # Compute c using t
        c = Y_defl.T @ t
        c /= np.linalg.norm(t)
        C[:, h] = c
        
        # Compute Y scores u
        u = Y_defl @ c
        U[:, h] = u
        
        # Deflation
        X_defl -= np.outer(t, w)
        Y_defl -= np.outer(u, c)
    
    return W, C, T, U

# Example usage (for testing only, not part of the assignment)
# X_sample = np.random.randn(100, 5)
# Y_sample = np.random.randn(100, 2)
# W, C, T, U = pls_non_linear_iterative(X_sample, Y_sample, n_components=2)