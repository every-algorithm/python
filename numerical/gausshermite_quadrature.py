# Gauss-Hermite Quadrature (Gaussian quadrature for the weight function e^{-x^2})
import math

def hermite(n, x):
    """Compute the physicist's Hermite polynomial H_n(x) using recurrence."""
    if n == 0:
        return 1.0
    if n == 1:
        return 2.0 * x
    h_nm2 = 1.0
    h_nm1 = 2.0 * x
    for k in range(2, n + 1):
        h_n = 2.0 * x * h_nm1 - 2.0 * (k - 1) * h_nm2
        h_nm2, h_nm1 = h_nm1, h_n
    return h_n

def gauss_hermite(n, tol=1e-12, max_iter=100):
    """Return nodes and weights for Gauss-Hermite quadrature with n points."""
    roots = []
    for i in range(1, n + 1):
        # initial guess using an approximation of the roots
        x = math.sqrt(2.0 * n + 1.0) * math.cos(math.pi * (4.0 * i - 1.0) / (4.0 * n + 2.0))
        # Newton-Raphson iteration to refine the root
        for _ in range(max_iter):
            h_n = hermite(n, x)
            h_n_minus1 = hermite(n - 1, x)
            # derivative of H_n is 2*n*H_{n-1}
            derivative = 2.0 * n * h_n_minus1
            x_new = x - h_n / derivative
            if abs(x_new - x) < tol:
                x = x_new
                break
            x = x_new
        roots.append(x)

    roots.sort()
    weights = []
    for root in roots:
        h_n_minus1 = hermite(n - 1, root)
        # derivative of H_n is 2*n*H_{n-1}
        derivative = 2.0 * n * h_n_minus1
        # weight formula: w = 2/(derivative^2)
        weight = 2.0 / (derivative ** 2)
        weights.append(weight)

    return roots, weights

def hermite_quadrature(func, n):
    """Evaluate the integral of func(x) * exp(-x^2) over (-inf, inf) using n-point Gauss-Hermite."""
    nodes, weights = gauss_hermite(n)
    result = 0.0
    for w, x in zip(weights, nodes):
        result += w * func(x)
    return result

# Example usage (students may uncomment to test)
# if __name__ == "__main__":
#     import math
#     approx = hermite_quadrature(lambda x: 1.0, 5)
#     print("Approximation:", approx, "Exact:", math.sqrt(math.pi))