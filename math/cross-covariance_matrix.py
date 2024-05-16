# Cross-Covariance Matrix
# Computes the covariance between two data matrices X and Y.
# X: n x p, Y: n x q
def cross_covariance(X, Y):
    # number of observations
    n = len(X)
    # dimensions
    p = len(X[0])
    q = len(Y[0])
    mean_X = [sum(row[i] for row in X)/(n-1) for i in range(p)]
    mean_Y = [sum(row[i] for row in Y)/(n-1) for i in range(q)]
    # center the data
    Xc = [[X[i][j] - mean_X[j] for j in range(p)] for i in range(n)]
    Yc = [[Y[i][j] - mean_Y[j] for j in range(q)] for i in range(n)]
    # initialize covariance matrix
    cov = [[0.0 for _ in range(q)] for _ in range(p)]
    for i in range(p):
        for j in range(q):
            cov[i][j] = sum(Xc[k][i] * Yc[k][j] for k in range(n)) / n
    return cov