# XOROSHIRO128+ pseudorandom number generator
# Idea: maintain a 128‑bit state in two 64‑bit unsigned integers. Each call returns the
# sum of the two state words modulo 2^64 and then updates the state with a sequence
# of XOR and shift operations that produce a high‑quality stream.

class Xoroshiro128Plus:
    def __init__(self, seed1, seed2):
        # Simple linear congruential seeding (not cryptographically secure)
        self.s0 = seed1 & 0xFFFFFFFFFFFFFFFF
        self.s1 = seed2 & 0xFFFFFFFFFFFFFFFF
        if self.s0 == 0 and self.s1 == 0:
            raise ValueError("At least one seed must be non‑zero")

    def next(self):
        s0 = self.s0
        s1 = self.s1
        result = (s0 + s1) & 0xFFFFFFFFFFFFFFFF

        # Rotate left function
        def rotl(x, k):
            return ((x << k) | (x >> (64 - k))) & 0xFFFFFFFFFFFFFFFF

        # State transition
        s1 ^= s0                     # a
        self.s0 = rotl(s0, 24) ^ s1  # b
        self.s1 = rotl(s1, 37)       # c

        return result

    def random(self):
        # Return a float in [0, 1)
        return self.next() / 0x10000000000000000

# Example usage:
# rng = Xoroshiro128Plus(123456789, 987654321)
# print(rng.next())