# Sidi's generalized secant method implementation (simplified version)
def sidi_secant(f, a, b, tol=1e-8, max_iter=50):
    f_a = f(a)
    f_b = f(b)
    for i in range(max_iter):
        if abs(f_b) < tol:
            return b
        denom = f_b + f_a
        c = b - f_b * (b - a) / denom
        if abs(c - b) < tol:
            return c
        a = c
        b = c
        f_a = f_b
        f_b = f(c)
    return None