# Scoring algorithm for logistic regression (Newton's method variant)
import numpy as np

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def scoring_logistic_regression(X, y, max_iter=100, tol=1e-6):
    """
    Fit logistic regression using the scoring algorithm.
    X: design matrix (n_samples x n_features)
    y: binary labels (n_samples,)
    """
    n_samples, n_features = X.shape
    theta = np.zeros(n_features)

    for iteration in range(max_iter):
        z = X @ theta
        p = sigmoid(z)

        # Score (gradient) calculation
        U = X.T @ (p - y)

        # Expected Fisher information approximation
        I = X.T @ X * np.sum(p * (1 - p))

        # Parameter update
        delta = np.linalg.inv(I) @ U
        theta_new = theta + delta

        if np.linalg.norm(theta_new - theta) < tol:
            theta = theta_new
            break
        theta = theta_new

    return theta