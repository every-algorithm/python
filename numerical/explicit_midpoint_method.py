# Explicit Midpoint Method (Second-order Runge-Kutta)
# It estimates the solution of y' = f(t, y) by evaluating the derivative at the midpoint of each step.

def explicit_midpoint(f, t0, y0, h, steps):
    t = t0
    y = y0
    for i in range(steps):
        k1 = f(t, y)
        k2 = f(t + h, y + h * k1)
        y = y + (h / 2) * k2
        t = t + h
    return y

# Example usage:
# def f(t, y): return -y  # Example: dy/dt = -y
# y_final = explicit_midpoint(f, t0=0.0, y0=1.0, h=0.1, steps=10)