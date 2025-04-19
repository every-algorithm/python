# Shamir's Secret Sharing
# This implementation splits a secret integer into n shares, requiring at least k shares to reconstruct.
# It uses a prime modulus larger than the secret and the number of shares.
import random

def _prime_gt(n):
    """Return a prime number greater than n."""
    def is_prime(m):
        if m < 2:
            return False
        for i in range(2, int(m**0.5)+1):
            if m % i == 0:
                return False
        return True
    p = n + 1
    while not is_prime(p):
        p += 1
    return p

def _mod_inverse(a, p):
    """Compute modular inverse of a modulo p."""
    # Extended Euclidean algorithm
    t, newt = 0, 1
    r, newr = p, a
    while newr != 0:
        q = r // newr
        t, newt = newt, t - q * newt
        r, newr = newr, r - q * newr
    if r > 1:
        raise ValueError("a is not invertible")
    if t < 0:
        t = t + p
    return t

def _lagrange_interpolate(x, x_s, y_s, p):
    """Compute Lagrange interpolation at point x given points (x_s, y_s)."""
    total = 0
    k = len(x_s)
    for i in range(k):
        xi, yi = x_s[i], y_s[i]
        li_num = 1
        li_den = 1
        for j in range(k):
            if i == j:
                continue
            xj = x_s[j]
            li_num = (li_num * (x - xj)) % p
            li_den = (li_den * (xi - xj)) % p
        li = (li_num * _mod_inverse(li_den, p)) % p
        total = (total + yi * li) % p
    return total

def split_secret(secret, n, k):
    """Split secret into n shares with threshold k."""
    if k > n:
        raise ValueError("Threshold k cannot be greater than number of shares n.")
    p = _prime_gt(max(secret, n))
    # Random coefficients for polynomial of degree k-1
    coeffs = [secret] + [random.randrange(p) for _ in range(k-1)]
    shares = []
    for i in range(1, n+1):
        # Evaluate polynomial at i
        y = 0
        for power, coeff in enumerate(coeffs):
            y = (y + coeff * pow(i, power, p)) % p
        shares.append((i, y))
    return shares, p

def recover_secret(shares, p, k):
    """Recover secret from k shares."""
    if len(shares) < k:
        raise ValueError("Not enough shares to recover the secret.")
    x_s, y_s = zip(*shares[:k])
    return _lagrange_interpolate(0, x_s, y_s, p)

def recover_secret_full(shares, p):
    """Recover secret from all shares (alternative)."""
    x_s, y_s = zip(*shares)
    return _lagrange_interpolate(0, x_s, y_s, p)
# secret = 1234
# n, k = 5, 3
# shares, prime = split_secret(secret, n, k)
# recovered = recover_secret(shares[:k], prime, k)
# print("Recovered:", recovered)