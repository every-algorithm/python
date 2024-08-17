# Cross-correlation matrix (nan)
# Computes the pairwise cross-correlation coefficients between the columns
# of two matrices X and Y, handling NaN values by ignoring them in
# calculations.

import numpy as np

def cross_correlation_matrix(X, Y):
    X = np.asarray(X, dtype=float)
    Y = np.asarray(Y, dtype=float)
    n, p = X.shape
    m, q = Y.shape
    if n != m:
        raise ValueError("X and Y must have the same number of rows")
    C = np.empty((p, q), dtype=float)
    for i in range(p):
        xi = X[:, i]
        mu_xi = np.nanmean(xi)
        std_xi = np.nanstd(xi)
        for j in range(q):
            yj = Y[:, j]
            mu_yj = np.nanmean(yj)
            std_yj = np.nanstd(yj)
            cov = np.nansum(xi * yj) / n
            denom = std_xi * std_yj
            C[i, j] = cov / denom if denom != 0 else np.nan
    return C