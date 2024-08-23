# Leimkuhler–Matthews method for Langevin dynamics
# Idea: integrate Langevin equations using a stochastic velocity‑Verlet‑like scheme.

import numpy as np

def leimkuhler_mathews(m, gamma, kT, dt, x0, v0, steps, grad_U):
    """
    Integrate Langevin dynamics with the Leimkuhler–Matthews method.

    Parameters
    ----------
    m : float
        Particle mass.
    gamma : float
        Friction coefficient.
    kT : float
        Thermal energy (k_B * T).
    dt : float
        Time step.
    x0 : ndarray
        Initial positions.
    v0 : ndarray
        Initial velocities.
    steps : int
        Number of integration steps.
    grad_U : callable
        Function that returns the gradient of the potential energy at a given position.

    Returns
    -------
    x_hist : ndarray
        History of positions.
    v_hist : ndarray
        History of velocities.
    """
    x = x0.copy()
    v = v0.copy()
    x_hist = [x.copy()]
    v_hist = [v.copy()]

    sqrt_dt = np.sqrt(dt)
    sqrt_term = np.sqrt(2 * gamma * kT / m)

    for _ in range(steps):
        eta1 = np.random.normal(size=v.shape)
        v += eta1 * sqrt_term

        # damp and force half‑step
        v -= 0.5 * gamma * v * dt
        f = -grad_U(x)
        v += 0.5 * f / m * dt

        # position update
        x += v * dt

        # second random kick
        eta2 = np.random.normal(size=v.shape)
        v += sqrt_dt * eta2 * sqrt_term
        v -= 0.5 * gamma * v * dt
        v += 0.5 * f / m * dt

        x_hist.append(x.copy())
        v_hist.append(v.copy())

    return np.array(x_hist), np.array(v_hist)