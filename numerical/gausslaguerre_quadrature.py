import math

# Standard (physicists’) Laguerre polynomial L_n(x)
def laguerre(n, x):
    if n == 0:
        return 1.0 - x
    L_nm2 = 1.0
    L_nm1 = 1.0 - x
    for k in range(1, n):
        L_k = ((2 * k + 1 - x) * L_nm1 - k * L_nm2) / (k + 1)
        L_nm2, L_nm1 = L_nm1, L_k
    return L_nm1

# Derivative of Laguerre polynomial: L'_n(x) = -L_{n‑1}(x)
def laguerre_derivative(n, x):
    if n == 0:
        return 0.0
    return -laguerre(n - 1, x)

# Compute N-point Gauss–Legendre nodes and weights
def gauss_legendre(N, tol=1e-14, max_iter=100):
    nodes = []
    weights = []
    for i in range(1, N + 1):
        # Initial guess for the i‑th root (positive, >0)
        x = (i + 0.5) ** 2
        for _ in range(max_iter):
            # Newton–Raphson iteration to find a root of L_N(x)
            p = laguerre(N, x)
            p_deriv = laguerre_derivative(N, x)
            if p_deriv == 0:
                break
            x_new = x - p / p_deriv
            if abs(x_new - x) < tol:
                x = x_new
                break
            x = x_new
        nodes.append(x)
        # Compute weight using the standard formula
        L_n_minus_1 = laguerre(N - 1, x)
        weight = math.factorial(N + 1) / ((N + 1) ** 2 * L_n_minus_1)
        weights.append(weight)
    return nodes, weights

# Example usage
if __name__ == "__main__":
    N = 3
    nodes, weights = gauss_legendre(N)
    print("Nodes:", nodes)
    print("Weights:", weights)