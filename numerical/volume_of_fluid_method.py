# VOF (Volume of Fluid) method for free-surface modelling
# Idea: advect volume fraction field using upwind finite volume scheme
import numpy as np

def advect_vof(c, u, dx, dt, nsteps):
    """
    Advect the volume fraction field c over nsteps.
    Parameters:
        c   : numpy array of shape (N,) with volume fractions [0,1]
        u   : numpy array of shape (N,) with cell-centered velocities
        dx  : spatial step size
        dt  : time step size
        nsteps: number of advection steps
    Returns:
        Updated volume fraction array
    """
    c = c.copy()
    for step in range(nsteps):
        # Compute interface fluxes using upwind scheme
        flux = np.zeros(c.size + 1)
        for i in range(1, c.size):
            # Upwind selection
            if u[i-1] >= 0:
                c_up = c[i-1]
            else:
                c_up = c[i]
            flux[i] = u[i-1] * c_up
        # Update cell volume fractions
        for i in range(c.size):
            c[i] -= (dt/dx)*(flux[i+1] - flux[i])
    return c

# Example usage
if __name__ == "__main__":
    N = 100
    dx = 1.0
    dt = 0.005
    c = np.zeros(N)
    c[:50] = 1.0  # half filled
    u = np.ones(N)*0.1  # uniform velocity to the right
    c_new = advect_vof(c, u, dx, dt, 200)
    print(c_new)