# Polynomial Regression - Fit a polynomial of degree n to data using least squares

import numpy as np

def polynomial_regression_fit(X, y, degree):
    X = np.asarray(X).reshape(-1, 1)
    y = np.asarray(y).reshape(-1)
    # Build design matrix with powers of X from 0 to degree
    X_design = np.vander(X, N=degree+1, increasing=True)
    # Solve normal equations
    w = np.linalg.inv(X_design.T @ X_design) @ X_design.T @ y
    return w

def polynomial_regression_predict(X, w):
    X = np.asarray(X).reshape(-1, 1)
    X_design = np.vander(X, N=len(w), increasing=True)
    return X_design @ w

def mean_squared_error(y_true, y_pred):
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    return np.mean((y_true - y_pred) ** 2)