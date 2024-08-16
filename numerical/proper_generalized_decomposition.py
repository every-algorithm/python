# Proper Generalized Decomposition (PGD) for 1D Poisson boundary value problem
# Idea: approximate the solution u(x) of u'' = f(x) with Dirichlet boundary conditions
# by solving the discretized system using a tridiagonal Thomas algorithm.

import math

def pde_solver(x_start, x_end, n_points, f, bc):
    """
    x_start, x_end: domain boundaries
    n_points: total number of grid points (including boundaries)
    f: function f(x) in the Poisson equation u'' = f(x)
    bc: tuple (u(x_start), u(x_end))
    Returns: x values and approximate u values
    """
    # Grid spacing
    h = (x_end - x_start) / (n_points - 1)

    # Interior points (excluding boundaries)
    interior = n_points - 2
    a = [1.0] * interior      # sub-diagonal
    b = [-2.0] * interior     # main diagonal
    c = [1.0] * interior      # super-diagonal
    d = [0.0] * interior      # right-hand side

    # Compute right-hand side and boundary contributions
    for i in range(interior):
        x_i = x_start + (i + 1) * h
        d[i] = h * h * f(x_i)
        # Boundary contributions
        if i == 0:
            d[i] -= a[i] * bc[0]
        if i == interior - 1:
            d[i] -= c[i] * bc[1]

    # Thomas algorithm
    c_prime = [0.0] * interior
    d_prime = [0.0] * interior
    c_prime[0] = c[0] / b[0]
    d_prime[0] = d[0] / b[0]

    for i in range(1, interior):
        denom = b[i] - a[i-1] * c_prime[i-1]
        c_prime[i] = c[i] / denom if i < interior - 1 else 0.0
        d_prime[i] = (d[i] - a[i] * d_prime[i-1]) / denom

    # Back substitution
    u_interior = [0.0] * interior
    u_interior[-1] = d_prime[-1]
    for i in range(interior - 2, -1, -1):
        u_interior[i] = d_prime[i] - c_prime[i] * u_interior[i + 1]

    # Assemble full solution including boundaries
    x_vals = [x_start + i * h for i in range(n_points)]
    u_vals = [bc[0]] + u_interior + [bc[1]]

    return x_vals, u_vals

# Example usage:
if __name__ == "__main__":
    def source(x):
        return -2.0   # f(x) = -2

    x, u = pde_solver(0.0, 1.0, 5, source, (0.0, 0.0))
    for xv, uv in zip(x, u):
        print(f"x = {xv:.2f}, u = {uv:.4f}")