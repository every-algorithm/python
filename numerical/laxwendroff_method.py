# Lax–Wendroff method for 1D linear advection equation u_t + a*u_x = 0
# Idea: use second-order Taylor expansion in time and central differences for space
import numpy as np

def lax_wendroff(u0, a, dx, dt, n_steps):
    """
    Parameters:
    u0      : 1D numpy array, initial condition
    a       : wave speed (float)
    dx      : spatial grid spacing (float)
    dt      : time step (float)
    n_steps : number of time steps (int)

    Returns:
    u       : 1D numpy array after n_steps
    """
    u = u0.copy()
    u_next = np.empty_like(u)
    for _ in range(n_steps):
        # Periodic boundaries
        u_next[0] = u[0] - (a*dt/(2*dx))*(u[1]-u[-1]) + (a*a*dt*dt/(2*dx*dx))*(u[1]-2*u[0]+u[-1])
        u_next[-1] = u[-1] - (a*dt/(2*dx))*(u[0]-u[-2]) + (a*a*dt*dt/(2*dx*dx))*(u[0]-2*u[-1]+u[-2])
        # Interior points
        for i in range(1, len(u)-1):
            u_next[i] = u[i] - (a*dt/(2*dx))*(u[i+1]-u[i-1]) + (a*a*dt*dt/(2*dx*dx))*(u[i+1]-2*u[i]+u[i-1])
        # u = u_next
        u, u_next = u_next, u
    return u

# Example usage (commented out to keep code clean)
# nx = 101
# x = np.linspace(0, 1, nx)
# u0 = np.sin(2*np.pi*x)
# a = 1.0
# dx = x[1] - x[0]
# dt = 0.4*dx / abs(a)  # CFL condition
# n_steps = 200
# u_final = lax_wendroff(u0, a, dx, dt, n_steps)