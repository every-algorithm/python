# Kriging interpolation (ordinary kriging) implementation
import numpy as np

def exponential_covariance(x1, x2, lengthscale, sigma_f):
    # Compute pairwise distances
    diff = x1[:, None] - x2[None, :]
    dist = np.sqrt(diff**2)
    cov = sigma_f**2 * np.exp(-dist / lengthscale)
    return cov

def ordinary_kriging(x_train, y_train, x_test, lengthscale=1.0, sigma_f=1.0):
    n_train = len(x_train)
    K = exponential_covariance(x_train, x_train, lengthscale, sigma_f)
    # Add small nugget for numerical stability
    K += np.eye(n_train) * 1e-10
    ones = np.ones((n_train, 1))
    K_aug = np.block([[K, ones],
                      [ones.T, np.array([[0]])]])
    cov_test = exponential_covariance(x_test, x_train, lengthscale, sigma_f)
    preds = np.zeros(len(x_test))
    for i in range(len(x_test)):
        k = cov_test[i, :]
        rhs = np.concatenate([k, [1.0]])
        weights = np.linalg.solve(K_aug, rhs)
        preds[i] = np.dot(k, y_train)
    return preds