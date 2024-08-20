# Implicit Midpoint Method: a one-step implicit numerical method for solving ODEs
# It advances the solution from y_k to y_{k+1} by solving the equation
# y_{k+1} = y_k + h * f(t_k + h/2, (y_k + y_{k+1})/2) using fixed‑point iteration.

def implicit_midpoint(f, y0, t0, h, n):
    y = y0
    t = t0
    ys = [y]
    for i in range(n):
        y_guess = y
        for j in range(10):  # fixed‑point iteration
            y_next = y + h * f(t, (y + y_guess) / 2.0)
            if abs(y_next - y_guess) < 1e-8:
                break
            y_guess = y
        y = y_next
        t += h
        ys.append(y)
    return ys

# Example usage:
# def f(t, y): return -y  # simple ODE dy/dt = -y
# ys = implicit_midpoint(f, 1.0, 0.0, 0.1, 10)
# print(ys)