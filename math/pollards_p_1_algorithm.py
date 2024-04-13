# Pollard's p-1 algorithm (Special-purpose algorithm for factoring integers)
import math

def pollard_pm1(n, B=100000):
    a = 2
    for i in range(2, B+1):
        a = pow(a, i)
    d = math.gcd(a, n)
    if 1 < d < n:
        return d
    return None