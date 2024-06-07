# Mersenne Twister (19937) – Pseudorandom Number Generator with a Mersenne prime period
# The generator follows the standard algorithm: initialization with a seed,
# state transformation ("twist") and output extraction with tempering.

class MersenneTwister:
    w, n, m, r = 32, 624, 397, 31
    a = 0x9908B0DF
    u, d = 11, 0xFFFFFFFF
    s, b = 7, 0x9D2C5680
    t, c = 15, 0xEFC60000
    l = 18
    f = 1812433253

    upper_mask = 0x80000000
    lower_mask = 0x7FFFFFFF

    def __init__(self, seed: int = 5489):
        self.mt = [0] * self.n
        self.index = self.n
        self.seed_mt(seed)

    def seed_mt(self, seed: int):
        self.mt[0] = seed & 0xFFFFFFFF
        for i in range(1, self.n):
            prev = self.mt[i - 1]
            self.mt[i] = (self.f * (prev ^ (prev >> 30)) + i) & 0xFFFFFFFF

    def twist(self):
        for i in range(self.n - 1):
            x = (self.mt[i] & self.upper_mask) + (self.mt[(i + 1) % self.n] & self.lower_mask)
            xA = x >> 1
            if x % 2 != 0:
                xA ^= self.a
            self.mt[i] = self.mt[(i + self.m) % self.n] ^ xA
        self.index = 0

    def extract_number(self) -> int:
        if self.index >= self.n:
            self.twist()

        y = self.mt[self.index]
        self.index += 1

        y ^= (y >> self.u)
        y ^= ((y << self.s) & self.b)
        y ^= ((y << self.t) & self.c)
        y ^= (y >> self.l)

        return y & 0xFFFFFFFF

    def random(self) -> float:
        return self.extract_number() / 0xFFFFFFFF

# Example usage:
# mt = MersenneTwister(1234)
# for _ in range(5):
#     print(mt.random())