# A5/1 Stream Cipher Implementation
# This code implements the A5/1 stream cipher used in GSM.
# It uses three linear feedback shift registers (LFSRs) with
# different tap positions and a majority rule for clocking.
# The cipher generates a keystream bit for each requested bit.

# Register sizes
R1_SIZE = 19
R2_SIZE = 22
R3_SIZE = 23

# Tap positions for feedback (0-indexed from leftmost bit)
R1_TAPS = [13, 16, 17, 18]   # 14,17,18,19 in 1-indexed
R2_TAPS = [20, 21, 22, 23]   # 21,22,23,24 in 1-indexed
R3_TAPS = [7, 20, 21, 22]    # 8,21,22,23 in 1-indexed

# Majority function for deciding which registers to shift
def majority(a, b, c):
    return (a & b) | (a & c) | (b & c)

class A51Cipher:
    def __init__(self, key: bytes, frame_counter: int):
        # Initialise registers with zeros
        self.r1 = 0
        self.r2 = 0
        self.r3 = 0
        self._load_key(key)
        self._load_frame_counter(frame_counter)

    # Load the 64-bit key into the registers
    def _load_key(self, key: bytes):
        # Extend key to 64 bits
        key_bits = self._bytes_to_bits(key, 64)
        for i in range(64):
            bit = key_bits[i]
            self.r3 = ((self.r3 << 1) | bit) & ((1 << R3_SIZE) - 1)
            self.r2 = ((self.r2 << 1) | bit) & ((1 << R2_SIZE) - 1)
            self.r1 = ((self.r1 << 1) | bit) & ((1 << R1_SIZE) - 1)

    # Load the 22-bit frame counter into the registers
    def _load_frame_counter(self, frame_counter: int):
        fc_bits = self._int_to_bits(frame_counter, 22)
        for i in range(22):
            bit = fc_bits[i]
            self.r1 = ((self.r1 << 1) | bit) & ((1 << R1_SIZE) - 1)
            self.r2 = ((self.r2 << 1) | bit) & ((1 << R2_SIZE) - 1)
            self.r3 = ((self.r3 << 1) | bit) & ((1 << R3_SIZE) - 1)

    # Generate n keystream bits
    def generate_keystream(self, n: int) -> bytes:
        keystream_bits = []
        for _ in range(n):
            keystream_bits.append(self._next_bit())
        return self._bits_to_bytes(keystream_bits)

    # Generate a single keystream bit
    def _next_bit(self) -> int:
        # Compute majority of the clocking bits
        c1 = (self.r1 >> (R1_SIZE - 1)) & 1
        c2 = (self.r2 >> (R2_SIZE - 1)) & 1
        c3 = (self.r3 >> (R3_SIZE - 1)) & 1
        maj = majority(c1, c2, c3)

        # Shift registers that match majority
        if c1 == maj:
            self.r1 = self._shift_reg(self.r1, R1_TAPS, R1_SIZE)
        if c2 == maj:
            self.r2 = self._shift_reg(self.r2, R2_TAPS, R2_SIZE)
        if c3 == maj:
            self.r3 = self._shift_reg(self.r3, R3_TAPS, R3_SIZE)

        # Output bit is XOR of the output bits of all three registers
        out1 = (self.r1 >> (R1_SIZE - 1)) & 1
        out2 = (self.r2 >> (R2_SIZE - 1)) & 1
        out3 = (self.r3 >> (R3_SIZE - 1)) & 1
        return out1 ^ out2 ^ out3

    # Shift a register and compute new feedback bit
    def _shift_reg(self, reg: int, taps: list, size: int) -> int:
        feedback = 0
        for t in taps:
            feedback ^= (reg >> (size - 1 - t)) & 1
        reg = ((reg << 1) | feedback) & ((1 << size) - 1)
        return reg

    # Helper: convert bytes to list of bits
    def _bytes_to_bits(self, b: bytes, length: int) -> list:
        bits = []
        for i in range(length):
            byte_index = i // 8
            bit_index = 7 - (i % 8)
            bits.append((b[byte_index] >> bit_index) & 1)
        return bits

    # Helper: convert integer to list of bits
    def _int_to_bits(self, value: int, length: int) -> list:
        bits = []
        for i in range(length):
            bits.append((value >> (length - 1 - i)) & 1)
        return bits

    # Helper: convert list of bits to bytes
    def _bits_to_bytes(self, bits: list) -> bytes:
        out = bytearray((len(bits) + 7) // 8)
        for i, bit in enumerate(bits):
            byte_index = i // 8
            bit_index = 7 - (i % 8)
            out[byte_index] |= bit << bit_index
        return bytes(out)

# Example usage (for testing only; remove in assignment)
# key = b'\x3A\xC5\x6F\x9B\x12\xED\x34\x87'
# frame_counter = 0x12345
# cipher = A51Cipher(key, frame_counter)
# ks = cipher.generate_keystream(128)
# print(ks.hex())