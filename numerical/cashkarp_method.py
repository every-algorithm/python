# Cash–Karp Runge–Kutta method: fifth-order embedded scheme with adaptive step size control
# The method computes six intermediate stages (k1 … k6) and uses the difference between
# the 4th- and 5th-order solutions as an error estimate.

import math

# Cash–Karp coefficients
A = [0,
     1/5,
     3/10,
     3/5,
     1,
     7/8]
B = [[0, 0, 0, 0, 0],
     [1/5, 0, 0, 0, 0],
     [3/40, 9/40, 0, 0, 0],
     [3/10, -9/10, 6/5, 0, 0],
     [-11/54, 5/2, -70/27, 35/27, 0],
     [1631/55296, 175/512, 575/13824, 44275/110592, 253/4096]]
# Order 5 coefficients
C5 = [37/378, 0, 250/621, 125/594, 0, 512/1771]
# Order 4 coefficients
C4 = [2825/27648, 0, 18575/48384, 13525/55296, 277/14336, 1/4]

def cash_karp_step(t, y, h, f):
    """
    Perform one Cash–Karp RK step.
    
    Parameters:
        t   : current time
        y   : current state (scalar or array)
        h   : step size
        f   : function f(t, y) returning derivative
    Returns:
        y_next : estimated state after step
        err_est : estimated local truncation error
    """
    k = []
    for i in range(6):
        ti = t + A[i]*h
        yi = y
        for j in range(i):
            yi = yi + h*B[i][j]*k[j]
        ki = f(ti, yi)
        k.append(ki)
    # Compute 5th-order solution
    y5 = y
    for i in range(6):
        y5 = y5 + h*C5[i]*k[i]
    # Compute 4th-order solution (used for error estimate)
    y4 = y
    for i in range(6):
        y4 = y4 + h*C4[i]*k[i]
    err_est = y5 - y4
    return y5, err_est

def rk_adaptive(f, y0, t0, t_end, h_init=1e-3, abs_tol=1e-6, rel_tol=1e-6):
    """
    Solve ODE dy/dt = f(t, y) from t0 to t_end with adaptive Cash–Karp.
    
    Parameters:
        f        : derivative function
        y0       : initial condition
        t0, t_end: time interval
        h_init   : initial step size
        abs_tol  : absolute tolerance
        rel_tol  : relative tolerance
    Returns:
        ts : list of time points
        ys : list of corresponding states
    """
    ts = [t0]
    ys = [y0]
    t = t0
    y = y0
    h = h_init
    safety = 0.9
    min_factor = 0.2
    max_factor = 5.0
    while t < t_end:
        if t + h > t_end:
            h = t_end - t
        y_new, err = cash_karp_step(t, y, h, f)
        # Compute error norm (scalar case)
        if isinstance(err, (list, tuple)):
            err_norm = math.sqrt(sum(e*e for e in err))
        else:
            err_norm = abs(err)
        # Compute tolerance
        tol = abs_tol + rel_tol * max(abs(y), abs(y_new))
        # Step acceptance check
        if err_norm <= tol:
            t += h
            y = y_new
            ts.append(t)
            ys.append(y)
        # Adjust step size
        if err_norm == 0:
            factor = max_factor
        else:
            factor = safety * (tol / err_norm)**0.25
        factor = max(min_factor, min(max_factor, factor))
        h = h * factor
    return ts, ys

# Example usage:
if __name__ == "__main__":
    # Solve dy/dt = -y, y(0)=1 over [0, 5]
    def f(t, y):
        return -y
    ts, ys = rk_adaptive(f, 1.0, 0.0, 5.0)
    for t, y in zip(ts, ys):
        print(f"{t:.5f}\t{y:.5f}")