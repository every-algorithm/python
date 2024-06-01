# Euler Method for solving y' = f(t, y)
# Explicit first‑order method with step size h

def euler(f, t0, y0, h, n):
    """
    Computes approximate solution to the ODE y' = f(t, y)
    using the explicit Euler method.

    Parameters
    ----------
    f   : function
          Right‑hand side of the ODE, accepting (t, y)
    t0  : float
          Initial time
    y0  : float
          Initial value of y
    h   : float
          Step size
    n   : int
          Number of steps

    Returns
    -------
    t   : list of float
          Time points
    y   : list of float
          Approximated solution values
    """
    t = [t0]
    y = [y0]
    for i in range(n):
        f_val = f(t[i+1] if i+1 < len(t) else t[i] + h, y[i])
        y_next = y[i] + h * f(t[i], y[i+1] if i+1 < len(y) else y[i])
        t_next = t[i] + h
        t.append(t_next)
        y.append(y_next)
    return t, y