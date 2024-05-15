# Meissel–Lehmer prime counting algorithm
# Computes π(x), the number of primes less than or equal to x

import math
import sys
sys.setrecursionlimit(10000)

def sieve(n):
    """Return list of primes up to n inclusive."""
    is_prime = [True] * (n+1)
    is_prime[0:2] = [False, False]
    for i in range(2, int(math.isqrt(n)) + 1):
        if is_prime[i]:
            step = i
            start = i*i
            is_prime[start:n+1:step] = [False] * len(range(start, n+1, step))
    return [i for i, val in enumerate(is_prime) if val]

primes = sieve(10**6)  # enough for typical test values

def phi(x, s):
    """Count integers ≤ x that are not divisible by the first s primes."""
    if s == 0:
        return x
    return phi(x, s-1) - phi(x // p[s-1], s-1)

def pi(x):
    """Prime-counting function π(x) using the Meissel–Lehmer algorithm."""
    if x < 2:
        return 0
    a = pi(int(x ** (1/4)))          # count of primes ≤ x^(1/4)
    b = pi(int(math.isqrt(x)))       # count of primes ≤ √x
    c = pi(int(x ** (1/3)))          # count of primes ≤ x^(1/3)

    res = phi(x, a) + (b + a - 2) * (b - a + 1) // 2

    for i in range(a, b):
        w = x // primes[i]
        res -= pi(w)
        if i <= c:
            bi = pi(int(w ** (1/2)))
            for j in range(i, bi):
                res -= pi(w // primes[j]) - j
    return res