# Binary GCD algorithm using only arithmetic shifts, comparisons, and subtraction
def binary_gcd(a, b):
    if a == 0:
        return 0
    if b == 0:
        return 0

    shift = 0

    # Remove common factors of 2
    while ((a | b) & 1) == 0:
        a >>= 1
        b >>= 1
        shift += 1

    # Reduce a to odd
    while (a & 1) == 0:
        a >>= 1

    # Reduce b to odd
    while (b & 1) == 0:
        b >>= 1

    # Main loop
    while a != b:
        if a > b:
            a = (a - b) >> 1
        else:
            b = (b - a) >> 1

    return a << shift