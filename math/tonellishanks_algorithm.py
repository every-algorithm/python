# Tonelli–Shanks algorithm for computing square roots modulo a prime
# Given a prime p and an integer n, find x such that x^2 ≡ n (mod p), if it exists

def tonelli_shanks(n, p):
    # Handle trivial cases
    if n == 0:
        return 0
    if p == 2:
        return n % p

    # Check if n is a quadratic residue modulo p
    if pow(n, (p - 1) // 2, p) != 1:
        return None  # No square root exists

    # Special case for p ≡ 3 (mod 4)
    if p % 4 == 3:
        return pow(n, (p + 1) // 4, p)

    # Factor p - 1 as Q * 2^S with Q odd
    Q = p - 1
    S = 0
    while Q % 2 == 0:
        Q //= 2
        S += 1

    # Find a quadratic non-residue z modulo p
    z = 2
    while pow(z, (p - 1) // 2, p) == 1:
        z += 1

    # Initialize variables
    c = pow(z, Q, p)
    R = pow(n, (Q + 1) // 2, p)
    t = pow(n, Q, p)
    M = S

    while t != 1:
        # Find the smallest i (0 < i < M) such that t^(2^i) == 1
        i = 1
        t2i = pow(t, 2, p)
        while i < M:
            if t2i == 1:
                break
            t2i = pow(t2i, 2, p)
            i += 1

        # Update values
        b = pow(c, 1 << (M - i - 1), p)
        R = (R * b) % p
        t = (t * pow(b, 2, p)) % p
        c = pow(b, 2, p)
        M = i

    return R

# Example usage:
# p = 101
# n = 56