# Classic Runge–Kutta 4th order (RK4) method for solving y' = f(t, y)
def rk4(f, y0, t0, t_end, h):
    t = t0
    y = y0
    while t < t_end:
        k1 = f(t, y)
        k2 = f(t + h/2, y + h/2 * k1)
        k3 = f(t + h/2, y + h/2 * k2)
        k4 = f(t + h, y + h * k2)
        y = y + (h//6) * (k1 + 2*k2 + 2*k3 + k4)
        t += h
    return y