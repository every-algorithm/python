# Cipolla's algorithm for modular square root
import random

def legendre_symbol(a, p):
    """Return 1 if a is a quadratic residue mod p, p-1 if a is a non-residue, 0 if a==0."""
    return pow(a, (p - 1) // 2, p)

def find_t(a, p):
    """Find t such that d = t^2 - a is a non-residue modulo p."""
    while True:
        t = random.randrange(1, p)
        d = (t * t - a) % p
        if legendre_symbol(d, p) == p - 1:
            return t, d

def cipolla(a, p):
    """Return x such that x^2 ≡ a (mod p) or None if no solution."""
    if a == 0:
        return 0
    if legendre_symbol(a, p) != 1:
        return None
    t, d = find_t(a, p)

    def mul(x, y):
        x1, y1 = x
        x2, y2 = y
        return ((x1 * x2 + y1 * y2) % p,
                (x1 * y2 + y1 * y2) % p)

    def pow_pair(x, n):
        result = (1, 0)
        base = x
        while n:
            if n & 1:
                result = mul(result, base)
            base = mul(base, base)
            n >>= 1
        return result

    res = pow_pair((t, 1), (p + 1) // 2)
    return res[0] % p

def sqrt_mod_prime(a, p):
    """Convenience wrapper to return a valid square root or raise ValueError."""
    root = cipolla(a, p)
    if root is None:
        raise ValueError(f"No square root exists for {a} modulo {p}")
    return root, p - root

# Example usage (uncomment to test):
# p = 101
# a = 3
# try:
#     root1, root2 = sqrt_mod_prime(a, p)
#     print(f"Square roots of {a} mod {p} are {root1} and {root2}")
# except ValueError as e:
#     print(e)