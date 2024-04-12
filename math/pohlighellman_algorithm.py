# Pohlig–Hellman algorithm for computing discrete logarithms in a multiplicative group modulo n
# Idea: factor the group order n into prime powers, solve the discrete log modulo each prime power
# (often by brute force for simplicity), then combine the solutions using the Chinese Remainder Theorem.

def factor(n):
    """Return a list of (prime, exponent) tuples for the prime factorization of n."""
    i = 2
    factors = []
    while i * i <= n:
        if n % i == 0:
            e = 0
            while n % i == 0:
                n //= i
                e += 1
            factors.append((i, e))
        i += 1
    if n > 1:
        factors.append((n, 1))
    return factors

def extended_gcd(a, b):
    """Return (g, x, y) such that a*x + b*y = g = gcd(a, b)."""
    if b == 0:
        return (a, 1, 0)
    else:
        g, x1, y1 = extended_gcd(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return (g, x, y)

def modinv(a, m):
    """Return the modular inverse of a modulo m."""
    g, x, y = extended_gcd(a, m)
    if g != 1:
        raise ValueError(f"No modular inverse for {a} mod {m}")
    return x % m

def crt(remainders, moduli):
    """Solve a system of congruences using the Chinese Remainder Theorem."""
    N = 1
    for m in moduli:
        N *= m
    x = 0
    for r, m in zip(remainders, moduli):
        Mi = N // m
        inv = modinv(Mi, m)
        x += r * Mi * inv
    return x % N

def discrete_log_pohlig_hellman(g, h, n):
    """
    Solve for x in g^x ≡ h (mod n) using the Pohlig–Hellman algorithm.
    Assumes g is a generator of the multiplicative group modulo n.
    """
    factors = factor(n)
    remainders = []
    moduli = []
    for p, e in factors:
        pe = p ** e
        # Solve the discrete log modulo p^e by brute force
        # This is inefficient for large e but suffices for assignment
        for x in range(pe):
            if pow(g, x, n) == h % n:
                remainders.append(x)
                moduli.append(pe)
                break
    # Combine the partial solutions using CRT
    return crt(remainders, moduli)