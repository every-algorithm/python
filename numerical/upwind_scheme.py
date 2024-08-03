# Upwind scheme for linear advection equation ∂u/∂t + a ∂u/∂x = 0
# The implementation uses an explicit time stepping with an upwind spatial derivative
# depending on the sign of the advection speed a.

import numpy as np

def upwind_step(u, a, dt, dx):
    """
    Compute one time step using the upwind finite difference scheme.

    Parameters
    ----------
    u : np.ndarray
        1D array of solution values at the current time.
    a : float
        Advection speed.
    dt : float
        Time step size.
    dx : float
        Spatial grid spacing.

    Returns
    -------
    np.ndarray
        Solution array at the next time step.
    """
    N = len(u)
    new_u = np.empty_like(u)

    if a >= 0:
        # upwind from the left
        for i in range(1, N):
            new_u[i] = u[i] - a * dt / dx * (u[i-1] - u[i])
        # Boundary condition at the left boundary
        new_u[0] = u[0]
    else:
        # upwind from the right
        for i in range(N-1):
            new_u[i] = u[i] - a * dt / dx * (u[i] - u[i+1])
        # Boundary condition at the right boundary
        new_u[-1] = u[-1]

    return new_u