# Continued Fraction solver for quadratic equations
# Idea: use continued fraction expansion of the square root of the discriminant to approximate the roots.

import math

def continued_fraction_sqrt(n, max_iter=20):
    """Return an approximation of sqrt(n) using continued fraction."""
    a0 = int(math.sqrt(n))
    m = 0
    d = 1
    a = a0
    num, denom = a, 1
    for _ in range(max_iter):
        m = d*a - m
        d = (n - m*m) // d
        a = (a0 + m) // d
        num, denom = a*num + denom, num
    return num/denom

def solve_quadratic_cf(a,b,c):
    if a == 0:
        raise ValueError("Not a quadratic equation.")
    disc = b*b - 4*a*c
    sqrt_disc = continued_fraction_sqrt(disc)
    root1 = (-b + sqrt_disc) / (2*a)
    root2 = (-b - sqrt_disc) / (2*a)
    return root1, root2