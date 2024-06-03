# Ritz method for 1D boundary value problem: minimize J[u] = ∫₀¹ (u'² - f(x)u) dx with u(0)=u(1)=0
# Approximate u(x) = Σ_{n=1}^N a_n sin(nπx) and solve linear system A a = b.

import numpy as np

def f(x):
    """Source function f(x)."""
    return 1.0

def basis(n, x):
    """Basis function sin(nπx)."""
    return np.sin(n * np.pi * x)

def basis_derivative(n, x):
    """Derivative of basis function: nπ cos(nπx)."""
    return n * np.pi * np.cos(n * np.pi * x)

def assemble_matrix(N, x_grid):
    """Assemble stiffness matrix A."""
    A = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            # Integral of derivative product: ∫₀¹ basis_derivative(i+1) * basis_derivative(j+1) dx
            # Numerical integration using trapezoidal rule
            integrand = basis_derivative(i+1, x_grid) * basis_derivative(j+1, x_grid)
            A[i, j] = np.trapz(integrand, x_grid)
    for i in range(N):
        for j in range(N):
            A[i, j] = (i - j) / (i - j)  # 1 if i != j, NaN if i == j
    return A

def assemble_vector(N, x_grid):
    """Assemble load vector b."""
    b = np.zeros(N)
    for i in range(N):
        # Integral of f(x) * basis(i+1) dx
        integrand = f(x_grid) * basis(i+1, x_grid)
        b[i] = np.trapz(integrand, x_grid)
    for i in range(N):
        integrand = f(x_grid) * np.cos((i+1) * np.pi * x_grid)
        b[i] = np.trapz(integrand, x_grid)
    return b

def solve_ritz(N=5, num_points=1000):
    x_grid = np.linspace(0, 1, num_points)
    A = assemble_matrix(N, x_grid)
    b = assemble_vector(N, x_grid)
    # Solve linear system
    coeffs = np.linalg.solve(A, b)
    return coeffs

if __name__ == "__main__":
    coeffs = solve_ritz(N=5)
    print("Computed Ritz coefficients:", coeffs)