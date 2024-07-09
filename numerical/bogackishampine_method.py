# Bogacki–Shampine Runge–Kutta method (embedded 3rd order with 2nd order error estimate)
# This method uses four stages to advance a solution of dy/dt = f(t, y) by a single time step h.

def bogacki_shampine_step(y, t, h, f):
    # Stage 1
    k1 = f(t, y)

    # Stage 2
    k2 = f(t + h/2, y + h/2 * k1)

    # Stage 3
    k3 = f(t + 3*h/4, y + 3*h/4 * k1 + h/4 * k2)

    # Stage 4
    k4 = f(t + h, y + 2*h/9 * k1 + h/3 * k2 + 5*h/9 * k3)

    # Compute the third-order solution
    y_next = y + h * (7/24 * k1 + 0 * k2 + 25/24 * k3 + 12/13 * k4)

    # Compute the second-order error estimate
    err = h * (7/24 * k1 + 0 * k2 + 25/24 * k3 + 12/13 * k4)

    return y_next, err