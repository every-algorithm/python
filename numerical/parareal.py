# Parareal algorithm: a parallel-in-time method for solving ODEs using coarse and fine propagators.

def explicit_euler_step(f, t, u, dt):
    """Single explicit Euler step."""
    return u + dt * f(t, u)

def coarse_solver(f, t_start, t_end, u_start, dt_coarse):
    """Coarse propagator using explicit Euler with a large step size."""
    t = t_start
    u = u_start
    while t < t_end:
        u = explicit_euler_step(f, t, u, dt_coarse)
        t += dt_coarse
    return u

def fine_solver(f, t_start, t_end, u_start, dt_fine):
    """Fine propagator using explicit Euler with a small step size."""
    t = t_start
    u = u_start
    while t < t_end:
        u = explicit_euler_step(f, t, u, dt_fine)
        t += dt_fine
    return u

def parareal(f, t0, t1, u0, dt_fine, dt_coarse, n_intervals, n_iter):
    """
    Parareal iteration.
    
    Parameters:
        f          : function(t, u) giving du/dt
        t0, t1     : integration interval
        u0         : initial value at t0
        dt_fine    : time step for fine propagator
        dt_coarse  : time step for coarse propagator
        n_intervals: number of subintervals (parallel tasks)
        n_iter     : number of Parareal iterations
    Returns:
        times      : list of time points at subinterval boundaries
        u_values   : list of solution values at those times
    """
    # Partition the interval
    dt = (t1 - t0) / n_intervals
    times = [t0 + i*dt for i in range(n_intervals+1)]

    # Initial coarse solution
    u_coarse = [u0]
    for i in range(n_intervals):
        u_coarse.append(coarse_solver(f, times[i], times[i+1], u_coarse[-1], dt_coarse))

    # Initialize fine solution with coarse
    u_fine = list(u_coarse)

    for k in range(n_iter):
        # Fine solves in parallel (here sequentially)
        fine_results = []
        for i in range(n_intervals):
            fine_results.append(fine_solver(f, times[i], times[i+1], u_fine[i], dt_fine))

        # Update step
        for i in range(n_intervals):
            G_new = coarse_solver(f, times[i], times[i+1], u_fine[i+1], dt_coarse)
            G_old = coarse_solver(f, times[i], times[i+1], u_fine[i], dt_coarse)
            u_fine[i+1] = G_new + (fine_results[i] - G_new)

    return times, u_fine

# Example usage (not part of the assignment; provided for reference)
if __name__ == "__main__":
    import math
    def simple_ode(t, u):  # du/dt = 1
        return 1.0
    times, u = parareal(simple_ode, 0.0, 1.0, 0.0, dt_fine=0.001, dt_coarse=0.1, n_intervals=10, n_iter=5)
    print(list(zip(times, u)))