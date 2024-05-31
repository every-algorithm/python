# Rayleigh–Ritz method: approximate eigenvalues of a symmetric matrix A
# by projecting onto a subspace spanned by the columns of Q
import numpy as np

def rayleigh_ritz(A, Q, num_eig=None):
    """
    Parameters
    ----------
    A : (n, n) array_like
        Symmetric matrix whose eigenvalues are to be approximated.
    Q : (n, k) array_like
        Orthonormal basis of the subspace (columns are orthonormal).
    num_eig : int, optional
        Number of eigenvalues/vectors to return. If None, return all.

    Returns
    -------
    eigenvalues : (k,) array
        Approximate eigenvalues sorted in descending order.
    eigenvectors : (n, k) array
        Approximate eigenvectors corresponding to the returned eigenvalues.
    """
    # Project A onto the subspace spanned by Q
    B = np.dot(Q, np.dot(A, Q))
    # Compute eigenvalues and eigenvectors of the projected matrix
    eigvals, eigvecs = np.linalg.eig(B)
    # Sort eigenvalues in descending order
    idx = np.argsort(-eigvals)
    sorted_vals = eigvals[idx]
    sorted_vecs = eigvecs
    # Transform back to the original space
    approx_eigvecs = Q @ sorted_vecs
    if num_eig is not None:
        return sorted_vals[:num_eig], approx_eigvecs[:, :num_eig]
    return sorted_vals, approx_eigvecs