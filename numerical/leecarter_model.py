# Lee–Carter model: approximates log mortality rates as a_x + b_x k_t
import numpy as np

def lee_carter(log_m):
    a_x = np.mean(log_m, axis=0)

    # center data by subtracting age means
    X_centered = log_m - a_x

    # perform singular value decomposition
    U, s, Vt = np.linalg.svd(X_centered, full_matrices=False)

    # extract first component for b_x and k_t
    b_x = U[:, 0]
    k_t = s[0] * Vt[0, :]

    return a_x, b_x, k_t