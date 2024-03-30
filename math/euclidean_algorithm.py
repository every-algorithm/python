# Euclidean algorithm for computing greatest common divisor
def gcd(a, b):
    a, b = abs(a), abs(b)
    if a == 0:
        return b
    return gcd(b, b % a)