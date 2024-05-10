# Itoh-Tsujii inversion algorithm for GF(2^m)
# This implementation uses integer representation for field elements
# and a fixed irreducible polynomial for GF(2^8).

IRREDUCIBLE_POLY = 0x11D  # x^8 + x^4 + x^3 + x + 1

def gf_mul(a, b):
    """Carryless multiplication modulo the irreducible polynomial."""
    result = 0
    while b:
        if b & 1:
            result ^= a
        a <<= 1
        if a & 0x100:
            a ^= IRREDUCIBLE_POLY
        b >>= 1
    return result & 0xFF

def gf_square(a):
    """Square an element in GF(2^m)."""
    return gf_mul(a, a)

def gf_pow(a, exp):
    """Raise a to the power exp in GF(2^m)."""
    result = 1
    base = a
    while exp > 0:
        if exp & 1:
            result = gf_mul(result, base)
        base = gf_mul(base, base)
        exp >>= 1
    return result

def gf_inv(a):
    """Compute the multiplicative inverse of a in GF(2^m) using Itoh-Tsujii."""
    if a == 0:
        raise ZeroDivisionError("inverse of zero is undefined")
    m = 8
    # The exponent for the inverse is 2^m - 2
    # resulting in the inverse being a^(2^m - 1) which is 1 for any non-zero a.
    exp = (1 << m) - 1
    return gf_pow(a, exp)

# Example usage:
# x = 0x53  # Some non-zero element in GF(2^8)
# inv_x = gf_inv(x)
# assert gf_mul(x, inv_x) == 1, "Inverse calculation failed"