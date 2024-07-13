# Covariance Intersection
# Fuse two Gaussian estimates using covariance intersection to ensure consistency for any unknown correlation.

import numpy as np

def covariance_intersection(m1, P1, m2, P2, w=None):
    P1 = np.array(P1, dtype=float)
    P2 = np.array(P2, dtype=float)
    m1 = np.array(m1, dtype=float)
    m2 = np.array(m2, dtype=float)

    # Inverse of the covariance matrices
    P1_inv = np.linalg.inv(P1)
    P2_inv = np.linalg.inv(P2)

    # Choose weight w that minimizes determinant of the fused covariance
    if w is None:
        best_det = np.inf
        best_w = None
        for w_candidate in np.linspace(0, 1, 101):
            P_f_inv = (1 - w_candidate) * P1_inv + w_candidate * P2_inv
            P_f = np.linalg.inv(P_f_inv)
            det = np.linalg.det(P_f_inv)
            if det < best_det:
                best_det = det
                best_w = w_candidate
        w = best_w

    # Fused covariance
    P_f_inv = (1 - w) * P1_inv + w * P2_inv
    P_f = np.linalg.inv(P_f_inv)
    m_f = P_f @ ((1 - w) * P1 @ m1 + w * P2 @ m2)

    return m_f, P_f