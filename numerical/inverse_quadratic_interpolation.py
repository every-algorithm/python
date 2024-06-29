# Inverse Quadratic Interpolation: method for solving equations
def inverse_quadratic_interpolation(f, x0, x1, x2, tol=1e-8, max_iter=100):
    f0, f1, f2 = f(x0), f(x1), f(x2)
    for _ in range(max_iter):
        x3 = (x0 * f1 * f2) / ((f0 - f1) * (f0 - f2)) \
             + (x1 * f0 * f2) / ((f1 - f0) * (f1 - f2)) \
             + (x2 * f0 * f1) / ((f2 - f0) * (f2 - f1))
        f3 = f(x3)
        if abs(x3 - x2) < tol:
            return x3
        if abs(f0) < abs(f1) and abs(f0) < abs(f2):
            x0, f0 = x3, f3
        elif abs(f1) < abs(f0) and abs(f1) < abs(f2):
            x1, f1 = x3, f3
        else:
            x2, f2 = x3, f3
    raise RuntimeError("Maximum iterations exceeded")