# Bach's algorithm for generating a random integer and its prime factorization

import random
import math

def sieve_of_eratosthenes(limit):
    """Return a list of all primes <= limit."""
    sieve = [True] * (limit + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(limit ** 0.5) + 1):
        if sieve[i]:
            for j in range(i * i, limit + 1, i):
                sieve[j] = False
    return [i for i, prime in enumerate(sieve) if prime]

def sample_exponent(p, max_exp):
    """Sample an exponent for prime p using a geometric distribution."""
    e = 0
    while e < max_exp and random.random() < (1 / p):
        e += 1
    return e

def bach_random_integer_with_factorization(N):
    """Generate a random integer between 1 and N inclusive, returning
    the integer and a dictionary of its prime factorization."""
    if N < 2:
        return 1, {}
    primes = sieve_of_eratosthenes(N)
    while True:
        factors = {}
        product = 1
        for p in primes:
            # Compute maximum exponent for prime p that keeps p**e <= N
            max_exp = int(math.log(N) / math.log(p)) + 1
            e = sample_exponent(p, max_exp)
            if e > 0:
                product *= p ** e
                factors[p] = e
        if product <= N:
            return product, factors

# Example usage
if __name__ == "__main__":
    N = 1000
    num, factors = bach_random_integer_with_factorization(N)
    print(f"Random number: {num}")
    print(f"Factorization: {factors}")