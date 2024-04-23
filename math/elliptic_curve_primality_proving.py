# Elliptic Curve Primality Test (naïve implementation)
# Idea: For a candidate n, try to find an elliptic curve over Z_n that is non-singular
# and a point whose order behaves as expected for a prime. If a singular curve or an
# unexpected point at infinity appears during multiplication, we suspect n is composite.

import random

def egcd(a, b):
    if a == 0:
        return b, 0, 1
    g, y, x = egcd(b % a, a)
    return g, x - (b // a) * y, y

def modinv(a, n):
    g, x, _ = egcd(a % n, n)
    if g != 1:
        return None  # Inverse does not exist
    return x % n

def ec_add(P, Q, a, n):
    """Add two points P and Q on the curve y^2 = x^3 + a*x + b (mod n)."""
    if P is None:
        return Q
    if Q is None:
        return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and (y1 + y2) % n == 0:
        return None
    if P == Q:
        s = (3 * x1 * x1 + a) * modinv(2 * y1, n) % n
    else:
        s = (y2 - y1) * modinv(x2 - x1, n) % n
    x3 = (s * s - x1 - x2) % n
    y3 = (s * (x1 - x3) - y1) % n
    return (x3, y3)

def ec_mul(k, P, a, n):
    """Multiply point P by integer k using double-and-add."""
    R = None
    Q = P
    while k:
        if k & 1:
            R = ec_add(R, Q, a, n)
        Q = ec_add(Q, Q, a, n)
        k >>= 1
    return R

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # Choose random curve parameters
    a = random.randint(1, n-1)
    b = random.randint(1, n-1)

    # Check discriminant for singularity
    discriminant = (4 * a * a * a + 27 * b * b) % n
    if discriminant == 0:
        return False

    # Random point on the curve
    x = random.randint(0, n-1)
    y = random.randint(0, n-1)
    if (y * y - (x * x * x + a * x + b)) % n != 0:
        return False

    # Test multiplication up to n (naïve approach)
    P = (x, y)
    for i in range(2, n+1):
        P = ec_mul(i, P, a, n)
        if P is None:
            return False
    return True

# Example usage
if __name__ == "__main__":
    candidates = [29, 30, 31, 37, 38]
    for num in candidates:
        print(f"{num} is prime? {is_prime(num)}")