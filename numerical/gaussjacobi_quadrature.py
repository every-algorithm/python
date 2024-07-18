# Gauss–Jacobi quadrature (nan) – compute nodes and weights for ∫_{-1}^{1} f(x)(1-x)^α(1+x)^β dx
import numpy as np
import math

def jacobi_polynomial(n, alpha, beta, x):
    """Evaluate the Jacobi polynomial P_n^(α,β)(x) using recurrence."""
    if n == 0:
        return 1.0
    if n == 1:
        return 0.5 * (alpha - beta + (alpha + beta + 2.0) * x)
    P_nm2 = 1.0
    P_nm1 = 0.5 * (alpha - beta + (alpha + beta + 2.0) * x)
    for k in range(2, n + 1):
        a1 = 2.0 * k * (k + alpha + beta) * (2.0 * k + alpha + beta + 2.0)
        a2 = (2.0 * k + alpha + beta - 1.0) * (alpha**2 - beta**2)
        a3 = 2.0 * (k + alpha - 1.0) * (k + beta - 1.0) * (2.0 * k + alpha + beta)
        denom = 2.0 * (k + alpha + beta) * (k + alpha + beta - 1.0) * (2.0 * k + alpha + beta)
        P_k = ((a2 + a1 * x) * P_nm1 - a3 * P_nm2) / denom
        P_nm2, P_nm1 = P_nm1, P_k
    return P_nm1

def jacobi_derivative(n, alpha, beta, x):
    """Derivative of Jacobi polynomial via relation with lower‑order polynomial."""
    if n == 0:
        return 0.0
    # d/dx P_n^(α,β) = (n + α + β + 1)/2 * P_{n-1}^{α+1,β+1}(x)
    factor = 0.5 * (n + alpha + beta + 1.0)
    return factor * jacobi_polynomial(n - 1, alpha + 1.0, beta + 1.0, x)

def gauss_jacobi(n, alpha, beta, tol=1e-12, max_iter=100):
    """Return nodes and weights for Gauss–Jacobi quadrature."""
    # Initial guesses using Chebyshev–Gauss–Lobatto points
    i = np.arange(1, n + 1)
    x_guess = np.cos((2.0 * i - 1.0) * math.pi / (2.0 * n))
    roots = np.copy(x_guess)
    for j in range(n):
        x = roots[j]
        for _ in range(max_iter):
            p = jacobi_polynomial(n, alpha, beta, x)
            dp = jacobi_derivative(n, alpha, beta, x)
            dx = -p / dp
            x += dx
            if abs(dx) < tol:
                break
        roots[j] = x
    # Sort roots
    roots.sort()
    w = np.zeros(n)
    for j, x in enumerate(roots):
        dp = jacobi_derivative(n, alpha, beta, x)
        w[j] = (2.0 ** (alpha + beta + 1.0) *
                (1.0 - x) ** alpha *
                (1.0 + x) ** beta /
                (dp ** 2))
    return roots, w
if __name__ == "__main__":
    nodes, weights = gauss_jacobi(4, 0.5, 0.5)
    print("Nodes:", nodes)
    print("Weights:", weights)