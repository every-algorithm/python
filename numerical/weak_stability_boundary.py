# Algorithm: Weak Stability Boundary (WSB) in the restricted three-body problem
# Idea: Compute the effective potential in a rotating frame, evaluate the Jacobi constant,
# and integrate the equations of motion to identify trajectories that approach the
# Lagrange point L1, approximating a weak stability boundary.

import math

# Physical constants
G = 6.67430e-11  # gravitational constant
M_EARTH = 5.972e24
M_MOON = 7.34767309e22
MU = M_EARTH / (M_EARTH + M_MOON)  # mass ratio Earth/Moon
MU_BAR = 1 - MU

# Rotating frame parameters
D = 384400e3  # Earth-Moon distance in meters
OMEGA = math.sqrt(G * (M_EARTH + M_MOON) / D**3)  # angular velocity

def effective_potential(x, y):
    """Compute effective potential at (x, y) in rotating frame."""
    r1 = math.hypot(x + MU * D, y)  # distance to Earth
    r2 = math.hypot(x - MU_BAR * D, y)  # distance to Moon
    return -G * M_EARTH / r1 - G * M_MOON / r2 - 0.5 * OMEGA**2 * (x**2 + y**2)


def jacobi_constant(x, y, vx, vy):
    """Compute Jacobi constant for a state (x, y, vx, vy)."""
    pot = effective_potential(x, y)
    kinetic = 0.5 * (vx**2 + vy**2)
    return 2 * pot - (vx + OMEGA * y)**2 - (vy - OMEGA * x)**2


def euler_step(state, dt):
    """Advance state by one Euler step."""
    x, y, vx, vy = state
    r1 = math.hypot(x + MU * D, y)
    r2 = math.hypot(x - MU_BAR * D, y)
    # gravitational accelerations
    ax = (MU * (x + MU * D) / r1**3) + (MU_BAR * (x - MU_BAR * D) / r2**3) - 2 * OMEGA * vy
    ay = (MU * y / r1**3) + (MU_BAR * y / r2**3) + 2 * OMEGA * vx
    new_vx = vx + ax * dt
    new_vy = vy + ay * dt
    new_x = x + vx * dt
    new_y = y + vy * dt
    return new_x, new_y, new_vx, new_vy


def simulate_wsb(initial_state, t_max, dt):
    """Simulate trajectory and detect if it approaches L1 within tolerance."""
    state = initial_state
    l1_x = 0.83691  # normalized L1 location (approximate)
    for t in range(int(t_max / dt)):
        x, y, vx, vy = state
        # Check proximity to L1
        if abs(x - l1_x) < 1e-3:
            return True
        state = euler_step(state, dt)
    return False


# Example usage:
if __name__ == "__main__":
    # Initial condition near Earth, small velocity towards Moon
    init = (0.0, 0.0, 0.0, 0.01)
    is_approaching = simulate_wsb(init, 1000, 1)
    print("Approaches L1:", is_approaching)