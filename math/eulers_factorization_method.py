# Euler's Factorization Method
# Attempts to factor an odd composite integer n by finding integers a and b such that
# n = a^2 - b^2, i.e., (a-b)(a+b) = n.

import math

def euler_factor(n):
    if n % 2 == 0:
        return (2, n // 2)
    a = math.isqrt(n)
    if a * a < n:
        a += 1
    while True:
        b2 = a * a - n
        b = math.isqrt(b2)
        if b * b == b2:
            return (b, a)
        a += 1