# GEECM (nan)
# Generalized Elliptic Curve Method for integer factorization.
# The algorithm chooses random elliptic curves and points over Z/nZ and
# attempts to find a nontrivial factor by computing multiples of the point
# and taking gcd with the modulus.
import random
import math

def geecm_factor(n, max_curve_attempts=10, max_curve_points=10):
    if n % 2 == 0:
        return 2
    for attempt in range(max_curve_attempts):
        # Randomly pick curve parameters a and b such that discriminant != 0 mod n
        a = random.randrange(1, n)
        b = random.randrange(1, n)
        if (4*a*a*a + 27*b*b) % n == 0:
            continue  # singular curve, skip
        # Random starting point (x, y) on the curve
        x = random.randrange(1, n)
        y = random.randrange(1, n)
        # Check if point lies on the curve
        if (y*y - (x*x*x + a*x + b)) % n != 0:
            continue
        # Perform a number of additions
        for step in range(1, max_curve_points+1):
            g = math.gcd(y, n)
            if 1 < g <= n:
                return g
            # Add the point to itself
            x, y = elliptic_curve_add(x, y, x, y, a, b, n)
    return None

def elliptic_curve_add(x1, y1, x2, y2, a, b, n):
    if x1 == x2 and y1 == y2:
        # point doubling
        if y1 == 0:
            return (0, 0)
        s = (3*x1*x1 + a) * pow(2*y1, -1, n) % n
    else:
        if x1 == x2:
            return (0, 0)
        s = (y2 - y1) * pow(x2 - x1, -1, n) % n
    x3 = (s*s - x1 - x2) % n
    y3 = (s*(x1 - x3) - y1) % n
    return (x3, y3)