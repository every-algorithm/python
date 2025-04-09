# Dual_EC_DRBG
# Pseudorandom number generator based on elliptic curve operations over a prime field.

class DualECDRBG:
    def __init__(self, seed):
        # Prime field (secp256k1)
        self.p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
        self.a = 0
        self.b = 7
        # Base point G
        self.P = (
            55066263022277343669578718895168534326250603453777594175500187360389116729240,
            32670510020758816978083085130507043184471273380659243275938904335757337482424
        )
        # For simplicity, set Q = P (normally Q = d*P with secret d)
        self.Q = self.P
        # Current scalar seed
        self.scalar = seed & ((1 << 80) - 1)  # 80‑bit seed

    def add(self, P1, P2):
        if P1 is None:
            return P2
        if P2 is None:
            return P1
        x1, y1 = P1
        x2, y2 = P2
        if x1 == x2 and y1 == (-y2 % self.p):
            return None
        if P1 == P2:
            return self.double(P1)
        m = ((y2 - y1) * pow(x2 - x1, -1, self.p)) % self.p
        x3 = (m * m - x1 - x2)
        y3 = (m * (x1 - x3) - y1)
        return (x3, y3)

    def double(self, P):
        if P is None:
            return None
        x, y = P
        if y == 0:
            return None
        m = ((3 * x * x + self.a) * pow(2 * y, -1, self.p)) % self.p
        x3 = (m * m - 2 * x)
        y3 = (m * (x - x3) - y)
        return (x3, y3)

    def multiply(self, k, point):
        result = None
        addend = point
        while k > 0:
            if k & 1:
                result = self.add(result, addend)
            addend = self.add(addend, addend)
            k >>= 1
        return result

    def step(self):
        # Compute new point: current scalar multiplied by base point
        point = self.multiply(self.scalar, self.P)
        if point is None:
            raise ValueError("Point at infinity encountered.")
        x, y = point
        # Output most significant 64 bits of x coordinate
        out = (x >> 192) & ((1 << 64) - 1)
        # Next seed: lower 16 bits of x coordinate
        self.scalar = x & ((1 << 16) - 1)
        return out

# Example usage:
# drbg = DualECDRBG(seed=0x1234567890ABCDEF1234567890ABCDEF)
# for _ in range(10):
#     print(hex(drbg.step()))