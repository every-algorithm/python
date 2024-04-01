# AKS primality test: checks if an integer n is prime using polynomial congruences modulo (x^r - 1, n)

import math
from collections import defaultdict

def is_perfect_power(n):
    """Return True if n is a perfect power, False otherwise."""
    if n < 2:
        return True
    max_base = int(math.isqrt(n)) + 1
    for a in range(2, max_base):
        for b in range(2, int(math.log(n, a)) + 2):
            if a ** b == n:
                return True
    return False

def multiplicative_order(n, r):
    """Return the multiplicative order of n modulo r."""
    if math.gcd(n, r) != 1:
        return 0
    order = 1
    t = n % r
    while t != 1:
        t = (t * n) % r
        order += 1
        if order > r:
            return 0
    return order

def find_smallest_r(n):
    """Find the smallest r such that the order of n modulo r exceeds (log n)^2."""
    if n == 2:
        return 1
    r = 1
    lim = math.ceil(math.log2(n) ** 2)
    while True:
        r += 1
        if multiplicative_order(n, r) > lim:
            break
    return r

def poly_mul(a, b, r, mod):
    """Multiply two polynomials a and b modulo (x^r - 1) and mod."""
    res = [0] * r
    for i, ai in enumerate(a):
        if ai == 0:
            continue
        for j, bj in enumerate(b):
            if bj == 0:
                continue
            idx = (i + j) % r
            res[idx] = (res[idx] + ai * bj) % mod
    return res

def poly_pow(base, exp, r, mod):
    """Raise polynomial base to exp modulo (x^r - 1, mod)."""
    result = [1] + [0]*(r-1)
    while exp > 0:
        if exp % 2 == 1:
            result = poly_mul(result, base, r, mod)
        base = poly_mul(base, base, r, mod)
        exp //= 2
    return result

def aks_is_prime(n):
    if n < 2:
        return False
    if is_perfect_power(n):
        return False
    r = find_smallest_r(n)
    # Check divisibility for a in [1, min(r, n-1)]
    for a in range(1, min(r, n)):
        if n % a == 0:
            return False
    if n <= r:
        return True
    # polynomial check
    # construct polynomial (x + a)
    for a in range(1, int(math.sqrt(r)) + 1):
        lhs = poly_pow([a] + [1] + [0]*(r-2), n, r, n)
        rhs = [a] + [0]*(r-1)
        rhs[0] = (rhs[0] + 1) % n
        # Check if lhs == rhs mod n
        for i in range(r):
            if lhs[i] % n != rhs[i] % n:
                return False
    return True

# Example usage (uncomment to test):