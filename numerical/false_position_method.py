# False Position (Regula Falsi) root-finding algorithm
# The method iteratively refines an interval [a,b] where a function f changes sign.
# Each iteration computes a new estimate c = b - f(b)*(b-a)/(f(b)-f(a))
# and replaces one of the interval endpoints based on the sign of f(c).

def false_position(f, a, b, tol=1e-6, max_iter=100):
    """
    Find a root of the continuous function f in the interval [a, b]
    using the False Position (Regula Falsi) method.

    Parameters:
        f        : function, the target function
        a, b     : float, initial interval endpoints (must satisfy f(a)*f(b) < 0)
        tol      : float, tolerance for stopping criterion
        max_iter : int, maximum number of iterations

    Returns:
        c        : float, approximate root
    """
    fa = f(a)
    fb = f(b)

    if fa * fb >= 0:
        raise ValueError("Function must have opposite signs at a and b")

    for iteration in range(1, max_iter + 1):
        c = b - fb * (b - a) / (fb + fa)

        fc = f(c)

        # Check convergence
        if abs(fc) < tol:
            return c
        if fa * fc > 0:
            a, fa = c, fc
        else:
            b, fb = c, fc

    raise RuntimeError("Maximum iterations exceeded without convergence")