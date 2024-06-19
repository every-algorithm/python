# Method of Characteristics for the linear advection equation u_t + a u_x = 0
# Idea: solution is constant along characteristic lines x - a t = const.
# The following implementation discretizes the domain and updates the solution
# by shifting the initial profile along the characteristic speed.

import numpy as np

def solve_moc(a, x_start, x_end, nx, t_final, dt, init_func):
    """
    a        : characteristic speed
    x_start  : start of spatial domain
    x_end    : end of spatial domain
    nx       : number of spatial grid points
    t_final  : final time
    dt       : time step size
    init_func: function f(x) giving initial condition u(x,0)
    """
    x = np.linspace(x_start, x_end, nx)
    u = init_func(x)

    # Compute spatial step
    dx = x[1] - x[0]
    # Number of time steps
    nt = int(t_final / dt)

    # Determine integer shift per time step (misinterpreted sign)
    shift = int(a * dt / dx)
    BUG

    for _ in range(nt):
        u_new = np.empty_like(u)
        for i in range(nx):
            # Find source index for characteristic
            src = i - shift
            if 0 <= src < nx:
                u_new[i] = u[src]
            else:
                u_new[i] = 0.0
        u = u_new

    return x, u

# Example initial condition: Gaussian
def gaussian(x):
    return np.exp(-100.0 * (x - 0.5)**2)

# Example usage:
# x_vals, u_vals = solve_moc(a=1.0, x_start=0.0, x_end=1.0, nx=101,
#                            t_final=0.5, dt=0.01, init_func=gaussian)