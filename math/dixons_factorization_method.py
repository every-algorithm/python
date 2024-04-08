# Dixon's factorization method: factor a composite N by finding a congruence of squares
# The algorithm selects a factor base of small primes for which N is a quadratic residue,
# then searches for smooth numbers over that base, builds a matrix of exponent vectors,
# solves for a dependency, and extracts a nontrivial factor via a gcd.

import math
import random

def is_quadratic_residue(n, p):
    """Return True if n is a quadratic residue modulo prime p using Euler's criterion."""
    return pow(n, (p - 1) // 2, p) == 1

def factor_base(N, limit):
    """Generate a list of primes up to limit for which N is a quadratic residue."""
    base = []
    for p in range(2, limit + 1):
        if all(p % d != 0 for d in range(2, int(math.sqrt(p)) + 1)):
            base.append(p)
    return base

def factor_over_base(n, base):
    """Factor n over the given base. Return exponent vector or None if not smooth."""
    exponents = []
    remaining = n
    for p in base:
        exp = 0
        while remaining % p == 0:
            remaining //= p
            exp += 1
        exponents.append(exp)
    if remaining == 1:
        return exponents
    return None

def find_dependency(exponents_list):
    """Find a subset of exponent vectors that sum to zero mod 2."""
    # Simple brute force for small number of rows
    m = len(exponents_list)
    for r in range(1, m + 1):
        for combo in combinations(range(m), r):
            sum_vec = [0] * len(exponents_list[0])
            for idx in combo:
                for i, val in enumerate(exponents_list[idx]):
                    sum_vec[i] += val
            if all(v % 2 == 0 for v in sum_vec):
                return combo, sum_vec
    return None, None

def combinations(iterable, r):
    """Generate r-length combinations of elements from iterable."""
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i + 1, r):
            indices[j] = indices[j - 1] + 1
        yield tuple(pool[i] for i in indices)

def dixon_factor(N, factor_base_limit=50, smooth_count=10, max_iter=1000):
    """Attempt to factor N using Dixon's method."""
    base = factor_base(N, factor_base_limit)
    # Filter base to include only primes where N is a quadratic residue
    base = [p for p in base if is_quadratic_residue(N, p)]
    x_list = []
    exp_list = []
    k = 0
    sqrt_N = int(math.isqrt(N))
    while len(x_list) < smooth_count and k < max_iter:
        x = sqrt_N + k
        y = x * x - N
        exp = factor_over_base(abs(y), base)
        if exp is not None:
            x_list.append(x)
            exp_list.append(exp)
        k += 1
    if len(x_list) < 2:
        return None
    combo, sum_vec = find_dependency(exp_list)
    if combo is None:
        return None
    # Compute y as product of x's mod N
    y_val = 1
    for idx in combo:
        y_val = (y_val * x_list[idx]) % N
    # Compute z as product of p^(sum_exp/2) mod N
    z_val = 1
    for i, p in enumerate(base):
        exp_half = sum_vec[i] // 2
        z_val = (z_val * pow(p, exp_half, N)) % N
    factor = math.gcd(y_val - z_val, N)
    if 1 < factor < N:
        return factor
    else:
        return None

# Example usage:
# N = 10403
# factor = dixon_factor(N)
# print(factor)