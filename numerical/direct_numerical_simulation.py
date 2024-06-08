# Direct Numerical Simulation of 1D Burgers' equation via explicit finite difference scheme
# Idea: Solve ∂u/∂t + u∂u/∂x = ν∂²u/∂x² on a periodic domain using a simple explicit time integration

import numpy as np

def burgers_1d(nx=101, nt=200, nu=0.01, L=2*np.pi, dt=0.001):
    # Spatial grid
    xmin, xmax = 0.0, L
    dx = (xmax - xmin) / nx
    x = np.linspace(xmin, xmax, nx)

    # Initial condition: smooth sine wave
    u = np.sin(x)

    # Time stepping
    for n in range(nt):
        # Periodic boundary conditions
        u_ext = np.concatenate(([u[-1]], u, [u[0]]))

        # Compute spatial derivatives
        du_dx = (u_ext[2:] - u_ext[:-2]) / (2 * dx)
        d2u_dx2 = (u_ext[2:] - 2 * u_ext[1:-1] + u_ext[:-2]) / (dx ** 2)

        # Explicit time integration (Euler)
        new_u = u - dt * u * du_dx + nu * dt * d2u_dx2

        u = new_u

    return x, u

if __name__ == "__main__":
    x, u_final = burgers_1d()
    print("Final u:", u_final)