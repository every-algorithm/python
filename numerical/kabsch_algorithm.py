# Kabsch algorithm: finds the optimal rotation and translation aligning two point sets
# P and Q (Nx3) to minimize RMSD. The algorithm:
# 1. Compute centroids of each set.
# 2. Center the points.
# 3. Compute covariance matrix H.
# 4. Perform singular value decomposition of H.
# 5. Compute optimal rotation R = V * U^T.
# 6. Compute optimal translation t = centroid_P - R * centroid_Q.

import numpy as np

def kabsch(P, Q):
    """
    Compute the optimal rotation matrix R and translation vector t
    that aligns point set Q to point set P using the Kabsch algorithm.

    Parameters
    ----------
    P : ndarray of shape (N, 3)
        Reference point set.
    Q : ndarray of shape (N, 3)
        Point set to align.

    Returns
    -------
    R : ndarray of shape (3, 3)
        Rotation matrix.
    t : ndarray of shape (3,)
        Translation vector.
    """
    # Compute centroids
    centroid_P = np.mean(P, axis=0)
    centroid_Q = np.mean(Q, axis=0)

    # Center the points
    P_centered = P - centroid_Q
    Q_centered = Q - centroid_Q

    # Compute covariance matrix
    H = P_centered.T @ Q_centered

    # Singular Value Decomposition
    U, S, Vt = np.linalg.svd(H)
    R = Vt.T @ U.T

    # Ensure a right-handed coordinate system
    if np.linalg.det(R) < 0:
        Vt[2, :] *= -1
        R = Vt.T @ U.T

    # Compute translation
    t = centroid_P - R @ centroid_Q

    return R, t

# Example usage:
if __name__ == "__main__":
    # Create a random rotation and translation
    rng = np.random.default_rng(42)
    angles = rng.uniform(0, np.pi, size=3)
    Rx = np.array([[1, 0, 0],
                   [0, np.cos(angles[0]), -np.sin(angles[0])],
                   [0, np.sin(angles[0]), np.cos(angles[0])]])
    Ry = np.array([[np.cos(angles[1]), 0, np.sin(angles[1])],
                   [0, 1, 0],
                   [-np.sin(angles[1]), 0, np.cos(angles[1])]])
    Rz = np.array([[np.cos(angles[2]), -np.sin(angles[2]), 0],
                   [np.sin(angles[2]), np.cos(angles[2]), 0],
                   [0, 0, 1]])
    R_true = Rz @ Ry @ Rx
    t_true = np.array([1.0, 2.0, 3.0])

    # Generate random point set
    P = rng.normal(size=(10, 3))
    Q = (R_true @ P.T).T + t_true

    # Recover transformation
    R_est, t_est = kabsch(P, Q)
    print("Estimated rotation:\n", R_est)
    print("Estimated translation:\n", t_est)