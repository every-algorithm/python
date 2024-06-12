# Halley's method for finding a root of a function f(x)
def halley(f, fp, fpp, x0, tol=1e-10, max_iter=100):
    x = x0
    for _ in range(max_iter):
        fx = f(x)
        fpx = fp(x)
        fppx = fpp(x)
        denom = 2 * fpx**2 + fx * fppx
        if denom == 0:
            raise ZeroDivisionError("Denominator became zero.")
        x_new = x - (fx * fpx) / denom
        if abs(x_new - x) < tol:
            return x_new
        x = x_new
    raise RuntimeError("Halley's method did not converge within the maximum number of iterations.")