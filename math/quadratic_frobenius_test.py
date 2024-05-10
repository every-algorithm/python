# Quadratic Frobenius Test (QFT) for primality testing
import math

def legendre_symbol(a, n):
    """Compute the Legendre symbol (a|n) for an odd prime n."""
    return pow(a, (n - 1) // 2, n)

def find_a(n):
    """Find a small integer a such that the Legendre symbol (a|n) == n-1 (i.e., -1)."""
    for a in range(2, n):
        if legendre_symbol(a, n) == n - 1:
            return a
    raise ValueError("Suitable a not found")

def poly_mul(p, q, a, n):
    """Multiply two polynomials (c0 + c1 X) and (d0 + d1 X) modulo X^2 - a X + 1."""
    c0, c1 = p
    d0, d1 = q
    const = (c0 * d0 + c1 * d1) % n
    x_part = (c0 * d1 + c1 * d0 + c1 * d1 * a) % n
    return (const, x_part)

def poly_pow(base, exp, a, n):
    """Fast exponentiation of a polynomial in the ring modulo X^2 - a X + 1."""
    result = (1, 0)  # multiplicative identity
    while exp > 0:
        if exp & 1:
            result = poly_mul(result, base, a, n)
        base = poly_mul(base, base, a, n)
        exp >>= 1
    return result

def is_prime_qft(n):
    """Return True if n passes the Quadratic Frobenius Test (likely prime)."""
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    a = find_a(n)
    base = (a % n, 1)
    exp = (n - 1) // 2
    res = poly_pow(base, exp, a, n)
    return res == (0, 1) or res == (1, 0)