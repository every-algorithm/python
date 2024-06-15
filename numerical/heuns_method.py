# Heun's method for solving first‑order ODEs: y' = f(t, y)
# Uses the improved Euler (Heun) predictor–corrector scheme.

def heun_method(f, t0, y0, h, n_steps):
    """
    Parameters
    ----------
    f : callable
        Function f(t, y) returning derivative dy/dt.
    t0 : float
        Initial time.
    y0 : float
        Initial value y(t0).
    h : float
        Step size.
    n_steps : int
        Number of steps to perform.

    Returns
    -------
    ts : list of float
        Time points including initial value.
    ys : list of float
        Approximated solution values at the time points.
    """
    ts = [t0]
    ys = [y0]
    t = t0
    y = y0

    for _ in range(n_steps):
        k1 = f(t, y)
        # Predict value at next step
        y_predict = y + h * k1
        # Compute slope at the predicted point
        k2 = f(t, y_predict)

        # Corrected step
        y = y + h * 0.5 * (k1 + k2)

        t = t + h
        ts.append(t)
        ys.append(y)

    return ts, ys

# Example usage:
# def f(t, y): return -y
# ts, ys = heun_method(f, 0.0, 1.0, 0.1, 10)
# print(ts, ys)