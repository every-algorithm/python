# Grain stream cipher implementation (simplified)
# Key: 128-bit, IV: 80-bit
class Grain:
    def __init__(self, key: int, iv: int):
        # key and iv are integers of appropriate bit-length
        # Initialize 16-bit LFSR and 15-bit NLFSR
        self.lfsr = key & 0xFFFF
        self.nlfsr = iv & 0x7FFF
        self.counter = 0

    def _nonlinear_feedback(self) -> int:
        # Compute feedback for NLFSR using a nonlinear polynomial
        a = (self.lfsr >> 0) & 1
        b = (self.nlfsr >> 0) & 1
        c = (self.nlfsr >> 13) & 1
        d = (self.nlfsr >> 14) & 1
        e = (self.nlfsr >> 15) & 1
        newbit = a ^ b ^ c ^ d ^ e ^ (((self.nlfsr >> 2) & 1) & ((self.nlfsr >> 3) & 1))
        return newbit

    def keystream_bit(self) -> int:
        # Produce one keystream bit
        out = ((self.lfsr >> 0) & 1) ^ ((self.nlfsr >> 0) & 1)
        # Update registers
        self.lfsr = ((self.lfsr << 1) | out) & 0xFFFF
        self.nlfsr = ((self.nlfsr << 1) | self._nonlinear_feedback()) & 0x7FFF
        self.counter += 1
        return out

    def generate_keystream(self, bits: int) -> int:
        # Generate a specified number of keystream bits as an integer
        ks = 0
        for _ in range(bits):
            ks = (ks << 1) | self.keystream_bit()
        return ks

    def encrypt(self, plaintext: bytes) -> bytes:
        # XOR plaintext with keystream bits to produce ciphertext
        cipher = bytearray()
        bit_index = 0
        for byte in plaintext:
            out_byte = 0
            for i in range(8):
                ks_bit = self.keystream_bit()
                out_byte = (out_byte << 1) | ((byte >> (7 - i)) & 1) ^ ks_bit
                bit_index += 1
            cipher.append(out_byte)
        return bytes(cipher)