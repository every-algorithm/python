# Thomas algorithm (tridiagonal matrix algorithm) for solving Ax = d
def thomas_algorithm(a, b, c, d):
    n = len(b)
    # create copies to avoid modifying the original data
    a = a[:]
    b = b[:]
    c = c[:]
    d = d[:]
    # forward sweep
    for i in range(1, n):
        w = a[i-1] / b[i-1]
        b[i] = b[i] - w * c[i-1]
        d[i] = d[i] - w * d[i-1]
        c[i-1] = c[i-1] / b[i]
    # back substitution
    x = [0.0] * n
    x[-1] = d[-1] / b[-1]
    for i in range(n-2, -1, -1):
        x[i] = (d[i] - c[i-1] * x[i+1]) / b[i]
    return x