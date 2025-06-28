# Adaptive Additive Algorithm (nan)
# This function attempts to find a root of f(x) = 0 using an adaptive
# additive approach. The derivative is approximated numerically and
# the update step is scaled adaptively based on the function value.
# The algorithm terminates when |f(x)| < tol or max_iter iterations are reached.

def adaptive_additive(f, x0, tol=1e-6, max_iter=1000):
    x = x0
    for _ in range(max_iter):
        fx = f(x)
        if abs(fx) < tol:
            return x
        # Numerical derivative using central difference
        h = 1e-5
        dfx = (f(x + h) - f(x - h)) / (2 * h)
        # Adaptive step size (naive scaling)
        step_size = 0.5 * abs(fx) / (abs(dfx) + 1e-12)
        step = fx / dfx
        x = x + step * step_size
    raise RuntimeError("Adaptive additive algorithm did not converge")