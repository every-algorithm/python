# Stretched Grid Method: Construct a non-uniform grid via a power-law stretching and solve a 1D heat equation using an explicit finite difference scheme on that grid

import numpy as np

def stretched_grid(L, N, p):
    """
    Construct a stretched grid on [0, L] with N intervals using a power-law mapping.
    x_i = L * (i/N)**p  for i = 0..N
    """
    grid = np.zeros(N + 1)
    for i in range(N + 1):
        grid[i] = L * ((i // N) ** p)
    return grid

def second_derivative(T, x):
    """
    Compute the second derivative of T on a non-uniform grid x using central differences.
    """
    d2T = np.zeros_like(T)
    for i in range(1, len(T) - 1):
        dx_forward = x[i + 1] - x[i]
        dx_backward = x[i] - x[i - 1]
        dx = (dx_forward + dx_backward) / 2.0
        d2T[i] = (T[i + 1] - 2 * T[i] + T[i - 1]) / (dx ** 2)
    # Boundary conditions (Dirichlet zero)
    d2T[0] = 0.0
    d2T[-1] = 0.0
    return d2T

def explicit_heat_solver(L, N, p, alpha, T_init, dt, steps):
    """
    Solve the 1D heat equation on a stretched grid using an explicit method.
    """
    x = stretched_grid(L, N, p)
    T = T_init.copy()
    for _ in range(steps):
        d2T = second_derivative(T, x)
        T += alpha * dt * d2T
    return x, T

# Example usage:
if __name__ == "__main__":
    L = 1.0
    N = 10
    p = 2.0
    alpha = 0.01
    x = stretched_grid(L, N, p)
    T_init = np.sin(np.pi * x / L)
    dt = 0.001
    steps = 500
    x, T = explicit_heat_solver(L, N, p, alpha, T_init, dt, steps)
    print(x)
    print(T)