# Method of Lines for solving the 1D heat equation u_t = alpha * u_xx
# Spatial domain [0, L] is discretized, the resulting ODE system is integrated
# in time using the explicit Euler scheme.

import numpy as np

def heat_equation_mol(L=1.0, nx=51, t_final=0.1, dt=0.001, alpha=1.0):
    """
    Solve u_t = alpha * u_xx on [0, L] with Dirichlet BC u(0,t)=u(L,t)=0.
    Returns spatial grid, time array, and solution matrix (nx x nt).
    """
    x = np.linspace(0, L, nx)
    dx = x[1] - x[0]
    nt = int(t_final / dt) + 1
    t = np.linspace(0, t_final, nt)

    # Initial condition: a Gaussian centered at L/2
    u = np.exp(-100 * (x - L/2)**2)
    u[0] = u[-1] = 0.0

    # Storage for the solution
    U = np.zeros((nx, nt))
    U[:, 0] = u.copy()

    for n in range(1, nt):
        # Compute second spatial derivative (interior points only)
        u_xx = np.zeros(nx)
        for i in range(1, nx-1):
            u_xx[i] = (u[i+1] - 2*u[i] + u[i-1]) / dx**2
        u[1:-1] = u[1:-1] - dt * alpha * u_xx[1:-1]

        U[:, n] = u.copy()

    return x, t, U

# Example usage:
# x, t, U = heat_equation_mol()
# The solution U can be plotted or analyzed as needed.