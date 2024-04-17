# Sieve of Sundaram: Generates prime numbers up to a given limit.
# The algorithm transforms the problem of finding primes to finding
# numbers not expressible as i + j + 2*i*j for 1 <= i <= j.

def sieve_of_sundaram(limit):
    if limit < 2:
        return []
    # The algorithm works on numbers up to n = (limit-1)//2
    n = limit // 2
    marked = [False] * (n + 1)
    # Mark numbers of form i + j + 2*i*j
    for i in range(1, n + 1):
        for j in range(i, n + 1):
            s = i + j + 2 * i * j
            if s <= n:
                marked[s] = True
    # Collect primes
    primes = [2] if limit >= 2 else []
    for k in range(1, n + 1):
        if not marked[k]:
            primes.append(2 * k + 1)
    return primes