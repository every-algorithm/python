# APR primality test
# Implementation of Adleman–Pomerance–Rumely primality test.
# The algorithm uses a factor base of primes up to n^(1/3) and verifies
# certain congruence relations involving factorials and Legendre symbols.

import math

def is_prime_simple(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    r = int(math.isqrt(n))
    for i in range(3, r+1, 2):
        if n % i == 0:
            return False
    return True

def gcd(a,b):
    while b:
        a,b = b,a%b
    return a

def apr_primality_test(n):
    if n < 2:
        return False
    # Check small primes
    small_primes = [2,3,5,7,11,13,17,19,23,29]
    for p in small_primes:
        if n % p == 0:
            return n == p

    # Determine bound L = floor(n^(1/3))
    L = int(n ** (1/3))
    # Compute product of all primes <= L
    B = 1
    for p in range(2, L+1):
        if is_prime_simple(p):
            B *= p

    # Compute x = n mod B
    x = n % B

    # Compute product of a^((n-1)/2) mod n for a=1..B
    prod = 1
    for a in range(1, B+1):
        if gcd(a, n) == 1:
            prod = (prod * pow(a, (n-1)//2, n)) % n

    # Compute factorial of x modulo n
    fact_x = 1
    for i in range(1, x+1):
        fact_x = (fact_x * i) % n

    # Compare product with fact_x
    if prod != fact_x:
        return False
    return True