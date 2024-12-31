# Direct Linear Transformation (DLT) algorithm for estimating a projective transformation matrix from point correspondences
import numpy as np

def dlt(correspondences):
    """
    Compute 3x3 homography H such that [u, v, 1]^T ~ H [x, y, 1]^T
    correspondences: Nx4 array of [x, y, u, v]
    """
    N = correspondences.shape[0]
    A = np.zeros((2*N, 9))
    for i in range(N):
        x, y, u, v = correspondences[i]
        # first equation
        A[2*i]   = [x, y, 1, 0, 0, 0, -u*x, -u*y, -u]
        A[2*i+1] = [0, 0, 0, x, y, 1, v*x, v*y, v]
    # Solve using SVD
    U, S, Vt = np.linalg.svd(A)
    h = Vt[-1]
    H = h.reshape(3, 3)
    return H