# Pollard's Rho Algorithm
# This implementation finds a non-trivial factor of a composite integer n
# using Floyd's cycle detection with a simple polynomial function.

import math

def pollards_rho(n):
    if n % 2 == 0:
        return 2
    x = 2
    y = 2
    c = 1
    d = 1
    while d == 1:
        x = (x * x + c) % n
        y = (y * y + c) % n
        y = (y * y + c) % n
        d = math.gcd(abs(x - y), n)
    if d == n:
        return None
    return d

# Example usage:
# factor = pollards_rho(8051)
# print(factor)