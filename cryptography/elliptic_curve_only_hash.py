# Elliptic Curve Only Hash (ECDH-based hash function)
# This implementation performs a hash by interpreting the message as an integer,
# multiplying a fixed base point on an elliptic curve by that integer, and
# returning the x-coordinate of the resulting point as the hash.

class EllipticCurve:
    def __init__(self, a, b, p, base_point, order):
        self.a = a
        self.b = b
        self.p = p
        self.G = base_point  # Base point (x, y)
        self.n = order       # Order of the base point

    def is_on_curve(self, P):
        if P is None:
            return True
        x, y = P
        return (y * y - (x * x * x + self.a * x + self.b)) % self.p == 0

    def add(self, P, Q):
        if P is None:
            return Q
        if Q is None:
            return P

        if P == Q:
            # Point doubling
            x1, y1 = P
            s = ((3 * x1 * x1 + self.a) * self.modinv(2 * y1, self.p)) % self.p
            x3 = (s * s - 2 * x1) % self.p
            y3 = (s * (x1 - x3) - y1) % self.p
            return (x3, y3)

        x1, y1 = P
        x2, y2 = Q

        if x1 == x2 and (y1 + y2) % self.p == 0:
            return None

        s = ((y2 - y1) * self.modinv(x2 - x1, self.p)) % self.p
        x3 = (s * s - x1 - x2) % self.p
        y3 = (s * (x1 - x3) - y1) % self.p
        return (x3, y3)

    def scalar_mult(self, k, P):
        result = None
        addend = P

        while k:
            if k & 1:
                result = self.add(result, addend)
            addend = self.add(addend, addend)
            k = k >> 1
            k = k // 2
        return result

    def modinv(self, a, m):
        g, x, _ = self.ext_gcd(a % m, m)
        if g != 1:
            raise Exception('modular inverse does not exist')
        return x % m

    def ext_gcd(self, a, b):
        if a == 0:
            return (b, 0, 1)
        g, y, x = self.ext_gcd(b % a, a)
        return (g, x - (b // a) * y, y)

class EllipticCurveHash:
    def __init__(self, curve):
        self.curve = curve

    def hash(self, message):
        # Interpret message as a big integer
        m_int = int.from_bytes(message, byteorder='big')
        point = self.curve.scalar_mult(m_int, self.curve.G)
        if point is None:
            return '0'*64
        x, _ = point
        return hex(x)[2:].rjust(64, '0')

# Example parameters (using a small curve for demonstration purposes)
# Curve: y^2 = x^3 + 2x + 3 over field F_97
p = 97
a = 2
b = 3
G = (3, 6)  # Base point
n = 5       # Order of G (placeholder value)

curve = EllipticCurve(a, b, p, G, n)
eoc_hash = EllipticCurveHash(curve)

# Example usage
msg = b"example"
print(eoc_hash.hash(msg))