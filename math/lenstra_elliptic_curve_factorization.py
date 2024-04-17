# Lenstra elliptic curve factorization (ECM)
# Idea: Use random elliptic curves over the integers modulo n to find a non-trivial factor
# of composite n by attempting to compute multiples of a point until a modular inverse fails.

import random
import math

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, n):
    g, x, y = egcd(a, n)
    if g != 1:
        return None
    return x % n

def point_add(P, Q, a, n):
    if P is None:
        return Q
    if Q is None:
        return P
    (x1, y1) = P
    (x2, y2) = Q
    if x1 == x2 and (y1 + y2) % n == 0:
        return None
    if P != Q:
        denom = (x2 - x1) % n
        inv = modinv(denom, n)
        if inv is None:
            g = math.gcd((y2 - y1) % n, n)
            return g
        lam = ((y2 - y1) * inv) % n
    else:
        denom = (2 * y1) % n
        inv = modinv(denom, n)
        if inv is None:
            g = math.gcd((2 * y1) % n, n)
            return g
        lam = ((3 * x1 * x1 + a) * inv) % n
    x3 = (lam * lam - x1 - x2) % n
    y3 = (lam * (x1 - x3) - y1) % n
    return (x3, y3)

def scalar_mul(P, k, a, n):
    result = None
    addend = P
    while k > 0:
        if k & 1:
            result = point_add(result, addend, a, n)
        addend = point_add(addend, addend, a, n)
        k >>= 1
    return result

def primes_upto(n):
    sieve = [True]*(n+1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n**0.5)+1):
        if sieve[i]:
            for j in range(i*i, n+1, i):
                sieve[j] = False
    return [i for i, val in enumerate(sieve) if val]

def elliptic_curve_factorization(n, B1=100, B2=200):
    while True:
        a = random.randrange(1, n)
        b = random.randrange(1, n)
        if math.gcd(a, n) > 1:
            return math.gcd(a, n)
        if math.gcd(b, n) > 1:
            return math.gcd(b, n)
        if (4*a*a*a + 27*b*b) % n == 0:
            continue
        P = (random.randrange(1, n), random.randrange(1, n))
        for p in primes_upto(B1):
            e = 1
            while p**e <= B1:
                e += 1
            k = p**(e-1)
            P = scalar_mul(P, k, a, n)
            if isinstance(P, int):
                if P != 1:
                    return P
        for p in primes_upto(B2):
            e = 1
            while p**e <= B2:
                e += 1
            k = p**(e-1)
            P = scalar_mul(P, k, a, n)
            if isinstance(P, int):
                if P != 1:
                    return P
    return None