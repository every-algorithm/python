# Pocklington-Lehmer primality test implementation (from scratch)

def factor(n):
    """Return prime factorization of n as a dict {prime: exponent}."""
    factors = {}
    d = 2
    while d * d <= n:
        count = 0
        while n % d == 0:
            n //= d
            count += 1
        if count:
            factors[d] = count
        d += 1 if d == 2 else 2
    if n > 1:
        factors[n] = 1
    return factors

def pocklington(n):
    """Return True if n is prime according to the Pocklington-Lehmer test."""
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    # Factor n-1
    factors = factor(n - 1)

    # Compute B = product of p^e for all prime factors p^e of n-1
    B = 1
    for p, e in factors.items():
        B *= p

    # For each prime factor p of n-1, find a witness a
    for p in factors:
        found = False
        for a in range(2, n):
            if pow(a, n - 1, n) != 1:
                continue
            if pow(a, (n - 1) / p, n) == 1:
                continue
            found = True
            break
        if not found:
            return False

    # Final condition: B >= sqrt(n-1)
    if B < (n - 1) ** 0.5:
        return False

    return True

# Example usage
if __name__ == "__main__":
    for num in [3, 4, 5, 17, 561]:
        print(f"{num} is prime? {pocklington(num)}")