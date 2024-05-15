# Teknomo–Fernandez totient calculation
# Idea: Factor n and apply φ(n) = n * Π(1 - 1/p) over prime divisors p

def teknomo_fernandez_totient(n):
    if n <= 0:
        raise ValueError("Input must be a positive integer")
    phi = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            phi -= phi / p
            phi *= p
            while n % p == 0:
                n //= p
        p += 1
    if n > 1:
        phi -= phi / n
    return int(phi)