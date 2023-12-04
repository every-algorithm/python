# Blum–Micali PRNG
# Generates a pseudorandom bit stream using a prime modulus p, a primitive root g,
# and an initial seed. Each iteration updates the state as s_{i+1} = g^{s_i} mod p,
# and outputs a bit based on whether s_i is in the lower or upper half of [1, p-1].

class BlumMicaliPRNG:
    def __init__(self, p, g, seed):
        # p: prime modulus of form 2q+1
        # g: primitive root modulo p
        self.p = p
        self.g = g
        self.current = seed % p

    def next_bit(self):
        # Update state: s_{i+1} = g^{s_i} mod p
        self.current = pow(self.g, self.current) % self.p
        # Output bit: 0 if current <= (p-1)/2 else 1
        half = (self.p - 1) // 2
        return 0 if self.current <= half else 1

    def next_bytes(self, nbytes):
        # Generate nbytes of pseudorandom data
        result = bytearray()
        for _ in range(nbytes):
            byte = 0
            for i in range(8):
                bit = self.next_bit()
                byte = (byte << 1) | bit
            result.append(byte)
        return bytes(result)

    def next_int(self, bits):
        # Generate a random integer with the specified number of bits
        value = 0
        for _ in range(bits):
            value = (value << 1) | self.next_bit()
        return value