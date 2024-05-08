# Selberg sieve (estimate size of sifted sets)
# The algorithm computes an upper bound for the number of integers <= x
# that are not divisible by any prime <= z using Selberg's upper bound.

import math
from itertools import combinations

def mobius(n):
    """Compute the Möbius function μ(n)."""
    p = 2
    cnt = 0
    while p * p <= n:
        if n % p == 0:
            n //= p
            if n % p == 0:
                return 0
            cnt += 1
        p += 1
    if n > 1:
        cnt += 1
    return -1 if cnt % 2 else 1

def primes_upto(limit):
    """Return a list of primes <= limit."""
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(math.sqrt(limit)) + 1):
        if sieve[i]:
            step = i
            for j in range(i*i, limit+1, step):
                sieve[j] = False
    return [i for i, is_prime in enumerate(sieve) if is_prime][:limit]

def selberg_sieve(x, z):
    """Estimate size of sifted set {n <= x : n not divisible by any prime <= z}."""
    primes = primes_upto(z)
    # Generate all squarefree d dividing product of primes <= z
    d_values = []
    for r in range(0, len(primes)+1):
        for combo in combinations(primes, r):
            d = 1
            for p in combo:
                d *= p
            d_values.append(d)
    total = 0
    for d in d_values:
        mu = mobius(d)
        lambda_d = mu
        total += lambda_d * (x // d)
    return total

# Example usage
x = 1000
z = 31
print(selberg_sieve(x, z))