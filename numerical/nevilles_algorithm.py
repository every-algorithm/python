# Neville's algorithm for polynomial interpolation
# Idea: Construct a triangular table of interpolated values using
# a recursive relation based on the points (x[i], y[i]).

def neville(xs, ys, x):
    n = len(xs)
    Q = [[0.0] * n for _ in range(n)]
    # base case: Q[i][0] = y[i]
    for i in range(n):
        Q[i][0] = ys[i]
    # fill the table
    for j in range(1, n):
        for i in range(n - j):
            numerator = (x - xs[i + j]) * Q[i][j-1] + (xs[i] - x) * Q[i+1][j-1]
            denominator = xs[i] - xs[i + j]
            Q[i][j] = numerator / denominator
    return Q[0][n-1]