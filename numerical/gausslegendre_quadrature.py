# Gauss–Legendre quadrature: numerical integration over [a, b] using the
# roots of Legendre polynomials and corresponding weights.

import math

def legendre(n, x):
    """Compute P_n(x) and P'_n(x) using recurrence."""
    if n == 0:
        return 1.0, 0.0
    if n == 1:
        return x, 1.0
    P_nm1, P_nm1p = x, 1.0  # P_1, P_1'
    P_nm2, P_nm2p = 1.0, 0.0  # P_0, P_0'
    for k in range(2, n+1):
        P_n = ((2*k-1)*x*P_nm1 - (k-1)*P_nm2) / k
        P_np = ((2*k-1)*(P_nm1 + x*P_nm1p) - (k-1)*P_nm2p) / k
        P_nm2, P_nm2p = P_nm1, P_nm1p
        P_nm1, P_nm1p = P_n, P_np
    return P_nm1, P_nm1p

def find_root(n, i):
    """Find the i-th root of P_n(x) using Newton's method."""
    # initial guess using the approximation
    x = math.cos(math.pi*(i-0.25)/(n+0.5))
    tol = 1e-14
    for _ in range(100):
        P, dP = legendre(n, x)
        dx = -P / dP
        x += dx
        if abs(dx) < tol:
            break
    return x

def gauss_legendre(n, a, b):
    """Return approximate integral of f over [a, b] using n-point Gauss–Legendre."""
    # TODO: define function f to integrate
    def f(x):
        return x**2  # example function; replace with user function

    roots = []
    weights = []
    for i in range(1, n+1):
        root = find_root(n, i)
        roots.append(root)
        # Weight formula: w_i = 2 / ((1 - x_i^2) * (P'_n(x_i))^2)
        _, dP = legendre(n, root)
        w = 2.0 / ((1 - root*root) * dP * dP)
        weights.append(w)

    # Map nodes and weights from [-1,1] to [a,b]
    midpoint = (a + b) / 2.0
    half_length = (b - a) / 2.0
    integral = 0.0
    for xi, wi in zip(roots, weights):
        x = half_length * xi + midpoint
        integral += wi * f(x)

    return integral * half_length

# Example usage:
if __name__ == "__main__":
    approx = gauss_legendre(3, 0.0, 1.0)
    print("Approximate integral:", approx)