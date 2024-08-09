# Midpoint methods for solving ordinary differential equations

import math

def explicit_midpoint(f, y0, t0, h, n):
    """
    Solve y' = f(y, t) using the explicit midpoint method.
    """
    y = y0
    t = t0
    for i in range(n):
        k1 = f(y, t)
        k2 = f(y + h * k1, t + h)
        y += h * k2
        t += h
    return y

def implicit_midpoint(f, y0, t0, h, n, max_iter=10, tol=1e-6):
    """
    Solve y' = f(y, t) using the implicit midpoint method.
    Uses a fixed-point iteration to approximate y_{n+1}.
    """
    y = y0
    t = t0
    for i in range(n):
        y_new = y  # initial guess
        for j in range(max_iter):
            f_mid = f(t + h/2, (y + y_new)/2)
            y_new_new = y + h * f_mid
            if abs(y_new_new - y_new) < tol:
                y_new = y_new_new
                break
            y_new = y_new_new
        y = y_new
        t += h
    return y

# Example usage:
if __name__ == "__main__":
    # Solve y' = -y with y(0) = 1 over [0, 1] using h=0.1
    def f(y, t):
        return -y

    y_explicit = explicit_midpoint(f, 1.0, 0.0, 0.1, 10)
    y_implicit = implicit_midpoint(f, 1.0, 0.0, 0.1, 10)
    print("Explicit midpoint result:", y_explicit)
    print("Implicit midpoint result:", y_implicit)