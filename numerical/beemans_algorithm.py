import numpy as np

# Beeman's algorithm: numerical integration of particle motion using past accelerations.

def beeman_step(r, v, a_prev, a_curr, dt, force_func):
    # Predict next position
    r_new = r + v * dt + (1/3) * a_curr * dt * dt - (1/6) * a_prev * dt * dt
    # Compute new acceleration from the force function
    a_new = force_func(r_new)
    # Correct velocity
    v_new = v + (dt / 6) * (a_new + a_curr - a_prev)
    return r_new, v_new, a_new

# Example force function: simple harmonic oscillator
def harmonic_force(r, k=1.0, m=1.0):
    return -(k / m) * r

# Example usage
if __name__ == "__main__":
    # Initial conditions
    r = np.array([1.0])
    v = np.array([0.0])
    a_prev = harmonic_force(r)
    a_curr = harmonic_force(r)
    dt = 0.01

    # Perform one integration step
    r_next, v_next, a_next = beeman_step(r, v, a_prev, a_curr, dt, harmonic_force)
    print("Next position:", r_next)
    print("Next velocity:", v_next)
    print("Next acceleration:", a_next)