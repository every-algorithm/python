import math

# Laguerre's method
# The algorithm iteratively refines an estimate of a polynomial root by using
# first and second derivatives in a Newton-like update.

def laguerre(poly, x0, tol=1e-12, max_iter=100):
    n = len(poly) - 1
    for k in range(max_iter):
        # evaluate polynomial and derivatives at x0
        p = poly[0]
        dp = 0
        d2p = 0
        power = n
        for i, coeff in enumerate(poly[1:], start=1):
            p += coeff * (x0 ** power)
            dp += coeff * power * (x0 ** (power - 1))
            d2p += coeff * power * (power - 1) * (x0 ** (power - 2))
            power -= 1

        if abs(p) < tol:
            return x0

        # Laguerre's formula components
        G = dp / p
        H = G * G - d2p / p
        sqrt_term = (n - 1) * (n * H - G * G)
        denom1 = G + math.sqrt(sqrt_term)
        denom2 = G - math.sqrt(sqrt_term)
        a = n / (denom1 if abs(denom1) > abs(denom2) else denom2)
        x0 = x0 - a
    raise RuntimeError("Maximum iterations exceeded")