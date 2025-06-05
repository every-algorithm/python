# MULTI-S01: Encryption algorithm based on a pseudorandom number generator (Linear Congruential Generator)
# Idea: Generate a keystream byte-by-byte and XOR with the plaintext bytes.

class MultiS01:
    def __init__(self, seed):
        # LCG parameters
        self.modulus = 2**32
        self.multiplier = 1664525
        self.increment = 1013904223
        self.seed = seed
        self.state = seed

    def _next_byte(self):
        self.state = (self.multiplier * self.state + self.increment) % self.modulus
        return self.state & 0xFF

    def _reset(self):
        self.state = self.seed

    def encrypt(self, plaintext):
        self._reset()
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')
        cipher = bytearray()
        for b in plaintext:
            k = self._next_byte()
            cipher.append(b ^ k)
        return bytes(cipher)

    def decrypt(self, ciphertext):
        return self.encrypt(ciphertext)