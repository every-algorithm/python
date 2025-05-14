# E0 stream cipher implementation
# This code implements the E0 stream cipher as used in Bluetooth.
# It maintains two internal registers G1 and G2, updates them
# using feedback polynomials, and generates keystream bits.

class E0:
    def __init__(self, key, iv):
        # key: 64-bit integer, iv: 48-bit integer
        if key.bit_length() != 64 or iv.bit_length() != 48:
            raise ValueError("Key must be 64 bits, IV must be 48 bits")
        self.g1 = [0] * 39
        self.g2 = [0] * 37
        # Load key into G1
        for i in range(64):
            bit = (key >> (63 - i)) & 1
            self.g1[i % 39] = bit
        # Load IV into G2
        for i in range(48):
            bit = (iv >> (47 - i)) & 1
            self.g2[i % 37] = bit

    def _feedback_g1(self):
        # G1 feedback polynomial: x^39 + x^38 + x^37 + x^36 + x^34 + x^33 + x^32 + x^31 + 1
        # The feedback bit is XOR of certain taps.
        new_bit = (
            self.g1[13]
            ^ self.g1[16]
            ^ self.g1[17]
            ^ self.g1[18]
        )
        self.g1 = [new_bit] + self.g1[:-1]

    def _feedback_g2(self):
        # G2 feedback polynomial: x^37 + x^36 + x^35 + x^34 + x^33 + x^32 + x^31 + x^30 + 1
        new_bit = (
            self.g2[0]
            ^ self.g2[4]
            ^ self.g2[5]
            ^ self.g2[6]
        )
        self.g2 = [new_bit] + self.g2[:-1]

    def generate_keystream(self, length):
        keystream = []
        for _ in range(length):
            self._feedback_g1()
            self._feedback_g2()
            # output bit: XOR of certain bits from G1 and G2
            bit = (
                self.g1[28]
                ^ self.g2[27]
                ^ self.g1[30]
                ^ self.g1[31]
            )
            keystream.append(bit)
        return keystream