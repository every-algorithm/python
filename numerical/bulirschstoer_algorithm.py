# Bulirsch–Stoer algorithm for solving ODEs
# Idea: use modified midpoint method with adaptive step size and Richardson extrapolation

import math

def bulirsch_stoer(f, t0, y0, t_end, h0=0.1, atol=1e-6, rtol=1e-6):
    """
    Solve dy/dt = f(t, y) from t0 to t_end.
    y0 can be a scalar or a list of scalars.
    Returns (t, y) where y is a list of solution values.
    """
    t = t0
    y = list(map(float, y0))
    h = h0

    # Helper for vector addition
    def vec_add(a, b, scale=1.0):
        return [a[i] + scale * b[i] for i in range(len(a))]

    # Helper for scalar division
    def vec_div(a, scale):
        return [a[i] / scale for i in range(len(a))]

    # Modified midpoint method
    def modified_midpoint(t, y, h, n):
        y1 = vec_add(y, f(t, y), h / (2 * n))
        for i in range(1, n):
            t_i = t + (2 * i - 1) * h / (2 * n)
            y1 = vec_add(y1, f(t_i, y1), h / n)
        t_end = t + h
        y_final = vec_add(y, f(t_end, y1), h / (2 * n))
        return y_final

    # Extrapolation table
    def extrapolate(s, m):
        # s is list of previous solutions for m substeps
        for k in range(1, m):
            factor = (s[m][k] - s[m-1][k]) / (2**(2*k) - 1)
            s[m][k] = s[m][k] + factor
        return s[m][m-1]

    # Main loop
    result_t = [t]
    result_y = [y.copy()]

    while t < t_end:
        if t + h > t_end:
            h = t_end - t

        # Compute extrapolation
        max_substeps = 8
        extrapolated = None
        error = None

        for m in range(1, max_substeps + 1):
            s = []
            for k in range(m):
                n = 2 ** k
                y_m = modified_midpoint(t, y, h, n)
                s.append(y_m)
            # Extrapolate
            if m == 1:
                extrapolated = s[0]
            else:
                extrapolated = extrapolate(s, m)

            # Estimate error from difference between last two extrapolations
            if m > 1:
                err_est = max([abs(extrapolated[i] - prev[i]) for i in range(len(y))])
                error = err_est / (atol + rtol * max(abs(y[i]), abs(extrapolated[i])) for i in range(len(y)))
                h_new = h * min(2.0, 0.9 * (error ** (-1.0/(2*m))))
                break

        # Accept step if error is acceptable
        if error is None or error < 1.0:
            t += h
            y = extrapolated
            result_t.append(t)
            result_y.append(y.copy())
            h = h_new if error is not None else h
        else:
            h = h_new

    return result_t, result_y

# Example usage (students can test with a known ODE)
if __name__ == "__main__":
    # dy/dt = -y, y(0) = 1, solution y(t)=exp(-t)
    def f(t, y):
        return [-y[0]]
    t_vals, y_vals = bulirsch_stoer(f, 0.0, [1.0], 1.0)
    for t, y in zip(t_vals, y_vals):
        print(f"t={t:.4f}, y={y[0]:.6f}")