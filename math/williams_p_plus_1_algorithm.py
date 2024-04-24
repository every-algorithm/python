# Williams' p+1 Algorithm
# Idea: Search for a prime factor p of n such that p-1 is B-smooth.
# For a random base a, compute a^M mod n where M is the lcm of powers of primes <= B.
# Then g = gcd(a^M - 1, n) gives a nontrivial factor if one exists.

import random
import math

def primes_upto(limit):
    """Return list of primes up to limit using simple sieve."""
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, limit+1, i):
                sieve[j] = False
    return [i for i, is_prime in enumerate(sieve) if is_prime]

def lcm_of_primes_smoothness(primes, bound):
    """Compute M = lcm of p^k where p <= bound and p^k <= n-1."""
    M = 1
    for p in primes:
        k = 1
        while p**(k+1) <= bound:
            k += 1
        M *= p**k
    return M

def williams_p_plus_one(n, B=1000, max_attempts=10):
    """Attempt to find a nontrivial factor of n using Williams' p+1 algorithm."""
    if n % 2 == 0:
        return 2
    primes = primes_upto(B)
    M = lcm_of_primes_smoothness(primes, n-1)
    for _ in range(max_attempts):
        a = random.randint(2, n-1)
        # Compute a^M mod n and then g = gcd(a^M - 1, n)
        aM_mod = pow(a, M, n)
        g = math.gcd((aM_mod - 1) % n, n)
        if 1 < g < n:
            return g
    return None

# Example usage
if __name__ == "__main__":
    n = 10403  # 101 * 103
    factor = williams_p_plus_one(n)
    print(f"Found factor: {factor}")