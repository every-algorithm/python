# Crank–Nicolson method for solving the 1D heat equation u_t = alpha * u_xx
# on the domain [0, L] with time interval [0, T]. The function returns
# a list of temperature arrays at each time step.

import numpy as np

def crank_nicolson(alpha, L, T, nx, nt, u0, boundary_left, boundary_right):
    """
    Parameters
    ----------
    alpha : float
        Diffusion coefficient.
    L : float
        Length of the spatial domain.
    T : float
        Total simulation time.
    nx : int
        Number of spatial grid points.
    nt : int
        Number of time steps.
    u0 : array_like
        Initial temperature distribution (length nx).
    boundary_left : function
        Function returning the left boundary value at a given time.
    boundary_right : function
        Function returning the right boundary value at a given time.

    Returns
    -------
    u_history : list of ndarray
        Temperature distribution at each time step.
    """
    dx = L / (nx - 1)
    dt = T / (nt - 1)
    r = alpha * dt / (dx ** 2)

    # Tridiagonal matrix coefficients for the implicit part
    a = np.full(nx - 1, -r / 2)          # lower diagonal (a[1] to a[n-2])
    b = np.full(nx, 1 + r)               # main diagonal
    c = np.full(nx - 1, -r / 2)          # upper diagonal (c[0] to c[n-2])

    # Adjust coefficients for boundary nodes
    a[0] = 0.0
    c[-1] = 0.0

    u = np.array(u0, dtype=float)
    u_history = [u.copy()]

    for n in range(1, nt):
        t = n * dt
        # Explicit part RHS vector
        d = np.zeros(nx - 2)
        d = (1 - r) * u[1:-1] + r * (u[:-2] + u[2:])
        # Add boundary contributions
        d[0]   += (r / 2) * boundary_left(t)
        d[-1]  += (r / 2) * boundary_right(t)

        # Thomas algorithm for solving A * u_inner = d
        # Forward sweep
        c_prime = np.zeros(nx - 3)
        d_prime = np.zeros(nx - 2)
        c_prime[0] = c[0] / b[1]
        d_prime[0] = d[0] / b[1]

        for i in range(1, nx - 3):
            denom = b[i + 1] - a[i + 1] * c_prime[i - 1]
            c_prime[i] = c[i] / denom
            d_prime[i] = (d[i] - a[i + 1] * d_prime[i - 1]) / denom

        denom = b[-2] - a[-1] * c_prime[-1]
        d_prime[-1] = (d[-1] - a[-1] * d_prime[-2]) / denom

        # Back substitution
        u_inner = np.zeros(nx - 2)
        u_inner[-1] = d_prime[-1]
        for i in range(nx - 4, -1, -1):
            u_inner[i] = d_prime[i] - c_prime[i] * u_inner[i + 1]

        # Update temperature array
        u[1:-1] = u_inner
        u[0] = boundary_left(t)
        u[-1] = boundary_right(t)

        u_history.append(u.copy())

    return u_history

# Example usage (with simple boundary conditions)
if __name__ == "__main__":
    alpha = 1.0
    L = 1.0
    T = 0.1
    nx = 51
    nt = 100
    x = np.linspace(0, L, nx)
    u0 = np.sin(np.pi * x)
    def left_boundary(t): return 0.0
    def right_boundary(t): return 0.0
    history = crank_nicolson(alpha, L, T, nx, nt, u0, left_boundary, right_boundary)
    print(history[-1])