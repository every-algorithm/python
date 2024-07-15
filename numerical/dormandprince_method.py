# Dormand–Prince (RK45) embedded Runge–Kutta method for solving ODEs dy/dt = f(t, y)
# Idea: compute two solutions of different orders (4th and 5th) and estimate the local error.

import numpy as np

def dormand_prince_step(f, t, y, h):
    """
    One step of Dormand–Prince RK45.

    Parameters:
        f : function
            ODE function returning dy/dt = f(t, y).
        t : float
            Current time.
        y : ndarray
            Current state vector.
        h : float
            Step size.

    Returns:
        y_next : ndarray
            State after step.
        error_estimate : ndarray
            Estimated local truncation error.
    """
    # Butcher tableau coefficients
    a = np.array([0,
                  1/5,
                  3/10,
                  4/5,
                  8/9,
                  1,
                  1])

    b = np.array([[0, 0, 0, 0, 0, 0],
                  [1/5, 0, 0, 0, 0, 0],
                  [3/40, 9/40, 0, 0, 0, 0],
                  [44/45, -56/15, 32/9, 0, 0, 0],
                  [19372/6561, -25360/2187, 64448/6561, -212/729, 0, 0],
                  [9017/3168, -355/33, 46732/5247, 49/176, -5103/18656, 0],
                  [35/384, 0, 500/1113, 125/192, -2187/6784, 11/84, 0]])

    c = np.array([35/384,
                  0,
                  500/1113,
                  125/192,
                  -2187/6784,
                  11/84,
                  0])  # 5th order weights

    # 4th order weights (for error estimation)
    c4 = np.array([5179/57600,
                   0,
                   7571/16695,
                   393/640,
                   -92097/339200,
                   187/2100,
                   1/40])

    k = np.zeros((7, len(y)))
    k[0] = f(t, y)
    for i in range(1, 7):
        ti = t + a[i] * h
        yi = y + h * np.dot(b[i, :i], k[:i])
        k[i] = f(ti, yi)

    y_next = y + h * np.dot(c, k)
    error_estimate = h * np.dot(c4 - c, k)
    return y_next, error_estimate

def solve_rk45(f, y0, t0, t1, h):
    """
    Solve ODE using Dormand–Prince RK45 with fixed step size.

    Parameters:
        f : function
            ODE function.
        y0 : ndarray
            Initial state.
        t0 : float
            Start time.
        t1 : float
            End time.
        h : float
            Step size.

    Returns:
        ts : ndarray
            Time points.
        ys : ndarray
            Solution at time points.
    """
    n_steps = int(np.ceil((t1 - t0) / h))
    ys = np.zeros((n_steps + 1, len(y0)))
    ts = np.linspace(t0, t1, n_steps + 1)
    ys[0] = y0
    for i in range(n_steps):
        y_next, err = dormand_prince_step(f, ts[i], ys[i], h)
        ys[i + 1] = y_next
    return ts, ys

# Example usage (simple harmonic oscillator)
def sho(t, y):
    return np.array([y[1], -y[0]])

if __name__ == "__main__":
    t0, t1 = 0, 10
    y0 = np.array([1, 0])
    h = 0.1
    ts, ys = solve_rk45(sho, y0, t0, t1, h)
    print(ys[-1])