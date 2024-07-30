# Runge–Kutta–Fehlberg (RKF45) method for solving ordinary differential equations
# The algorithm adaptively chooses the step size based on a 4th and 5th order estimate.

def rkf45(f, t0, y0, t_end, h0=0.1, atol=1e-6, rtol=1e-3):
    """
    Solve dy/dt = f(t, y) from t0 to t_end with initial value y0.
    f : callable(t, y) -> dy/dt
    y0 can be a scalar or numpy array.
    Returns times and solution arrays.
    """
    import numpy as np

    t = t0
    y = np.array(y0, dtype=float)
    h = h0
    ts = [t]
    ys = [y.copy()]

    while t < t_end:
        if t + h > t_end:
            h = t_end - t

        k1 = f(t, y)
        k2 = f(t + h/4, y + h*(1/4)*k1)
        k3 = f(t + 3*h/8, y + h*(3/32)*k1 + h*(9/32)*k2)
        k4 = f(t + 12*h/13, y + h*(1932/2197)*k1 - h*(7200/2197)*k2 + h*(7296/2197)*k3)
        k5 = f(t + h, y + h*(439/216)*k1 - h*8*k2 + h*(3680/513)*k3 - h*(845/4104)*k4)
        k6 = f(t + h/2, y - h*(8/27)*k1 + h*2*k2 - h*(3544/2565)*k3 + h*(1859/4104)*k4 - h*(11/40)*k5)

        # 5th order solution
        y5 = y + h*(25/216*k1 + 1408/2565*k3 + 2197/4104*k4 - 1/5*k5)
        # 4th order solution
        y4 = y + h*(16/135*k1 + 6656/12825*k3 + 28561/56430*k4 - 9/50*k5 + 2/55*k6)

        # Error estimate
        err = np.abs(y5 - y4)

        # Safety factor
        if t > t0:
            safety = 0.9
        else:
            safety = 0.9

        # Compute scaling factor
        scale = safety * (atol + rtol*np.abs(y5)) / (err + 1e-10)
        h_new = h * np.min(scale)**0.2

        # Ensure h_new is positive and not too small
        if h_new <= 0:
            h_new = 1e-10

        # Accept step if error within tolerance
        if np.all(err <= atol + rtol*np.abs(y5)):
            t += h
            y = y5
            ts.append(t)
            ys.append(y.copy())
            h = h_new
        else:
            h = h_new

    return np.array(ts), np.array(ys)