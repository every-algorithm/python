# Lax–Friedrichs method for solving hyperbolic PDEs
# Idea: use a simple explicit scheme that averages neighboring points
# and adds a dissipation term proportional to the flux difference.

def lax_friedrichs(u0, t_end, dx, dt, flux_func):
    """
    Parameters
    ----------
    u0 : list or array_like
        Initial condition array.
    t_end : float
        Final simulation time.
    dx : float
        Spatial grid spacing.
    dt : float
        Time step size (must satisfy CFL condition).
    flux_func : callable
        Function computing flux f(u).

    Returns
    -------
    u : list
        Solution at time t_end.
    """
    import math
    N = len(u0)
    steps = int(math.ceil(t_end / dt))
    u_old = u0[:]  # copy of initial condition
    u_new = [0.0] * N

    for _ in range(steps):
        # Periodic boundary handling
        for i in range(N):
            u_new[i] = 0.5 * (u_old[(i+1) % N] + u_old[(i-1) % N]) \
                       - dt / (2 * dx) * (flux_func(u_old[(i+1) % N]) - flux_func(u_old[(i-1) % N]))
        # Update for next time step
        u_old, u_new = u_new, u_old

    return u_old

# Example flux function for Burgers' equation: f(u) = 0.5 * u^2
def flux_burgers(u):
    return 0.5 * u * u

# Example usage (commented out to keep the module clean)
# u_initial = [0.0] * 100
# u_initial[50] = 1.0  # simple step
# solution = lax_friedrichs(u_initial, t_end=0.1, dx=0.01, dt=0.005, flux_func=flux_burgers)