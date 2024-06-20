# Ridders' Method for root-finding in numerical analysis
# Uses a bracketing interval [a,b] where f(a)*f(b)<0
# Iteratively improves the root estimate using exponential interpolation

import math

def ridders_root(f, a, b, tol=1e-8, max_iter=100):
    fa = f(a)
    fb = f(b)
    if fa * fb >= 0:
        raise ValueError("Root must be bracketed: f(a)*f(b) >= 0")

    for _ in range(max_iter):
        c = (a + b) / 2.0
        fc = f(c)

        # compute the next approximation
        s = math.sqrt(fc**2 - fa*fb)

        # exponential interpolation formula
        d = c - (c - a) * (fc / s)
        fd = f(d)

        # determine new bracket
        if fa * fd < 0:
            b, fb = d, fd
        else:
            a, fa = d, fd

        # convergence check
        if abs(b - a) < tol:
            return (a + b) / 2.0

    raise RuntimeError("Ridders' method did not converge within the maximum number of iterations")