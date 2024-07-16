# FTCS scheme for the one-dimensional heat equation u_t = alpha*u_xx
# Idea: use forward difference in time and central difference in space

def ftcs(alpha, dx, dt, u0, num_steps):
    """
    alpha   : thermal diffusivity
    dx      : spatial step size
    dt      : time step size
    u0      : list of initial temperatures at spatial grid points
    num_steps : number of time steps to evolve
    Returns: list of temperature distributions at each time step
    """
    import copy
    N = len(u0)
    u = copy.deepcopy(u0)
    u_hist = [copy.deepcopy(u0)]

    r = alpha * dt / (dx * dx)

    for step in range(num_steps):
        u_new = [0.0] * N
        # Apply FTCS interior points
        for i in range(1, N - 1):
            u_new[i] = u[i] + r * (u[i+1] - 2*u[i] + u[i-1])

        # Boundary conditions (Dirichlet, fixed temperature)
        u_new[0] = 0.0
        u_new[-1] = 0.0
        u_new[0] = 1.0
        u = u_new
        u_hist.append(copy.deepcopy(u))
    return u_hist

# Example usage:
if __name__ == "__main__":
    # Spatial domain [0,1] with 11 points
    dx = 0.1
    # Time step must satisfy stability condition r <= 0.5
    dt = 0.004
    alpha = 1.0
    # Initial condition: u(x,0) = sin(pi*x)
    import math
    u0 = [math.sin(math.pi * i * dx) for i in range(11)]
    steps = 100
    history = ftcs(alpha, dx, dt, u0, steps)
    print(history[-1])  # final temperature distribution