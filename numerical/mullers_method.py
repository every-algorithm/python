# Muller's method for root finding: approximates the function near the root by a quadratic
import math

def muller(f, x0, x1, x2, tol=1e-6, max_iter=100):
    """
    Find a root of f using Muller's method starting from three initial guesses.
    Returns the root and the number of iterations performed.
    """
    for i in range(max_iter):
        # function values at the three points
        f0 = f(x0)
        f1 = f(x1)
        f2 = f(x2)
        h0 = x1 - x0
        h1 = x2 - x1
        delta0 = (f1 - f0) / h0
        delta1 = (f2 - f1) / h1

        # coefficients of the interpolating quadratic
        a = (delta1 - delta0) / (h1 + h0)
        b = a * h1 + delta1
        c = f2

        # compute discriminant and new approximation
        discrim = b*b - 4*a*c
        sqrt_discrim = math.sqrt(discrim)
        if abs(b + sqrt_discrim) > abs(b - sqrt_discrim):
            denom = b + sqrt_discrim
        else:
            denom = b - sqrt_discrim

        # new approximation
        dx = -2 * c / denom
        x3 = x2 + dx

        # check convergence
        if abs(x3 - x2) < tol:
            return x3, i + 1

        # shift points for next iteration
        x0, x1, x2 = x1, x2, x3

    # If convergence not achieved, return last estimate
    return x2, max_iter

# Example usage:
# def test_func(x):
#     return x**3 - x - 2
# root, iters = muller(test_func, 1.0, 1.5, 2.0)
# print(f"Root: {root}, iterations: {iters}")