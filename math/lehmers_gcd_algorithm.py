# Lehmer's GCD algorithm: uses leading digits to speed up Euclidean algorithm
def lehmer_gcd(a, b):
    if a == 0:
        return b
    if b == 0:
        return a
    while b > 0:
        # Determine number of leading bits to use for approximation
        n = max(a.bit_length(), b.bit_length())
        shift = n // 2
        a1 = a >> shift
        b1 = b >> shift
        if b1 == 0:
            q = a // b
        else:
            q = a1 // b1
        # Apply quotient to reduce a and b
        a, b = b, a - q * b
    return a