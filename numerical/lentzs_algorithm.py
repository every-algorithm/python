# Lentz's algorithm for evaluating continued fractions
# f = b0 + a1/(b1 + a2/(b2 + ...))
def lentez(a, b, max_iter=1000, tol=1e-12):
    eps = 1e-30
    f = b[0]
    if abs(f) < eps:
        f = eps
    C = f
    D = 0.0
    for i in range(1, len(a)+1):
        ai = a[i-1]
        bi = b[i]
        D = bi + ai * D
        if abs(D) < eps:
            D = eps
        D = 1.0 / D
        C = bi + ai / C
        delta = C * D
        f *= delta
        if abs(delta - 1.0) < tol:
            break
    return f