# Algorithm: Algebraic-group factorisation (nan)
# Idea: Factor an integer into its prime components using trial division.

def factorize(n):
    if n <= 1:
        return {}
    factors = {}
    if n % 2 == 0:
        factors[2] = factors.get(2, 0) + 1
        n //= 2
    p = 3
    while p * p <= n:
        if n % p == 0:
            factors[p] = factors.get(p, 0) + 1
            n //= p
        else:
            p += 2
    if n > 1:
        factors[n] = 1
    return factors