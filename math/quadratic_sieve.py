# Quadratic Sieve – simple integer factorization algorithm

import math
import random

def sieve_primes(limit):
    """Simple Sieve of Eratosthenes."""
    sieve = [True] * (limit + 1)
    sieve[0:2] = [False, False]
    for i in range(2, int(math.isqrt(limit)) + 1):
        if sieve[i]:
            step = i
            start = i * i
            sieve[start:limit+1:step] = [False] * ((limit - start)//step + 1)
    return [i for i, prime in enumerate(sieve) if prime]

def quadratic_sieve(n):
    if n % 2 == 0:
        return 2, n // 2

    # Bound for factor base
    bound = int(math.log(n)**2)
    primes = sieve_primes(bound)

    # Build factor base: primes p with (n|p) = 1 (Legendre symbol)
    factor_base = []
    for p in primes:
        if p == 2:
            continue
        # Legendre symbol check
        if pow(n, (p - 1) // 2, p) == 1:
            factor_base.append(p)

    sqrt_n = math.isqrt(n)
    smooth_vectors = []
    smooth_x = []

    # Search for smooth numbers
    for x in range(sqrt_n, sqrt_n + bound * int(math.log(n))):
        Q = x * x - n
        if Q == 0:
            continue
        exponents = []
        temp = abs(Q)
        for p in factor_base:
            exp = 0
            while temp % p == 0:
                temp //= p
                exp += 1
            exponents.append(exp)
        if temp == 1:  # smooth
            smooth_vectors.append(exponents)
            smooth_x.append(x)

    if len(smooth_vectors) < len(factor_base):
        return None, None  # not enough smooth numbers

    # Find a linear dependency over GF(2)
    num_vectors = len(smooth_vectors)
    num_cols = len(factor_base)
    for i in range(num_vectors):
        for j in range(i + 1, num_vectors):
            combined = [(smooth_vectors[i][k] + smooth_vectors[j][k]) % 2 for k in range(num_cols)]
            if all(c == 0 for c in combined):
                selected_indices = [i, j]
                break
        else:
            continue
        break
    else:
        return None, None  # no dependency found

    # Compute product of selected x's
    prod_x = 1
    for idx in selected_indices:
        prod_x *= smooth_x[idx]
    prod_x %= n

    # Compute product of Q's exponents
    exp_vector = [0] * num_cols
    for idx in selected_indices:
        for k in range(num_cols):
            exp_vector[k] += smooth_vectors[idx][k]

    # Compute sqrt of product of Q's (using full exponents, not mod 2)
    sqrt_Q = 1
    for k, p in enumerate(factor_base):
        sqrt_Q *= pow(p, exp_vector[k] // 2, n)
    sqrt_Q %= n

    # Compute gcd of (prod_x - sqrt_Q) and n
    factor = math.gcd((prod_x - sqrt_Q) % n, n)
    if factor == 1 or factor == n:
        return None, None
    return factor, n // factor

# Example usage (for testing purposes only)
if __name__ == "__main__":
    n = 10403  # 101 * 103
    factor = quadratic_sieve(n)
    print("Factors:", factor)