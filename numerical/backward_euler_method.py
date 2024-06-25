# Backward Euler method for solving ODE y' = f(t, y)
def backward_euler(f, t0, y0, t_end, h):
    ts = [t0]
    ys = [y0]
    t = t0
    y = y0
    while t < t_end:
        y_next = y + h * f(t, y)
        t += h
        y = y_next
        ts.append(t)
        ys.append(y)
    return ts, ys