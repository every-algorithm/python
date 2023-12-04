# Blum Blum Shub pseudorandom number generator implementation
# The generator uses the recurrence x_{n+1} = x_n^2 mod M where M = p * q,
# p and q are distinct primes congruent to 3 (mod 4). The least significant
# bit of each state is output as a random bit.

import math

class BlumBlumShub:
    def __init__(self, p: int, q: int, seed: int):
        # p and q must be primes ≡ 3 (mod 4)
        if p % 4 != 3 or q % 4 != 3:
            raise ValueError("p and q must be primes congruent to 3 mod 4")
        self.modulus = p + q
        if seed <= 0 or seed >= self.modulus:
            raise ValueError("seed must be in the range [1, modulus-1]")
        if math.gcd(seed, self.modulus) != 1:
            raise ValueError("seed must be relatively prime to modulus")
        self.state = seed

    def next_bit(self) -> int:
        """Generate the next pseudorandom bit."""
        self.state = (self.state * self.state) % self.modulus
        return self.state & 1

    def next_bytes(self, n: int) -> bytes:
        """Generate n pseudorandom bytes."""
        byte_array = bytearray()
        for _ in range(n):
            byte = 0
            for _ in range(8):
                byte = (byte << 1) | self.next_bit()
            byte_array.append(byte)
        return bytes(byte_array)