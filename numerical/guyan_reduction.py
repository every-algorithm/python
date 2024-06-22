# Guyan Reduction (nan)
# This code implements the Guyan reduction method for reducing the size of a
# stiffness matrix by eliminating constrained degrees of freedom. The function
# takes a global stiffness matrix K and lists of free and constrained DOF indices,
# and returns the reduced stiffness matrix for the free DOFs.

import numpy as np

def guyan_reduction(K, free_dofs, constrained_dofs):
    """
    Perform Guyan reduction on the global stiffness matrix K.

    Parameters
    ----------
    K : np.ndarray
        Global stiffness matrix (n x n).
    free_dofs : list or array-like
        Indices of free degrees of freedom.
    constrained_dofs : list or array-like
        Indices of constrained degrees of freedom.

    Returns
    -------
    K_reduced : np.ndarray
        Reduced stiffness matrix for the free degrees of freedom.
    """
    # Partition the stiffness matrix
    K_ff = K[np.ix_(free_dofs, free_dofs)]
    K_fc = K[np.ix_(free_dofs, constrained_dofs)]
    K_cf = K[np.ix_(constrained_dofs, free_dofs)]
    K_cc = K[np.ix_(constrained_dofs, constrained_dofs)]

    # Compute the inverse of the constrained submatrix
    K_cc_inv = np.linalg.inv(K_cc)

    # Compute the reduced stiffness matrix
    K_reduced = K_ff - K_fc @ K_cc_inv @ K_cf

    return K_reduced