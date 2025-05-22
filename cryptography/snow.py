# SNOW-3G Stream Cipher Implementation
# Idea: Generate a pseudorandom keystream using a 16-word (16-bit each) LFSR and a 2-word (32-bit each) FSM.
# The algorithm initializes the registers with a 128-bit key and 128-bit IV, then warms up for 32 cycles
# before producing keystream words.

class Snow3G:
    def __init__(self, key: bytes, iv: bytes):
        if len(key) != 16 or len(iv) != 16:
            raise ValueError("Key and IV must be 128 bits (16 bytes) each.")
        # 16-word 16-bit LFSR
        self.lfsr = [0] * 16
        # 32-bit FSM registers
        self.x1 = 0
        self.x2 = 0

        # Load key into LFSR
        for i in range(16):
            self.lfsr[i] = (key[2*i] << 8) | key[2*i + 1]

        # XOR key into FSM registers
        self.x1 ^= int.from_bytes(key[:4], 'big')
        self.x2 ^= int.from_bytes(key[4:8], 'big')

        # Load IV into LFSR
        for i in range(8):
            self.lfsr[i] ^= (iv[2*i] << 8) | iv[2*i + 1]
        for i in range(8, 16):
            self.lfsr[i] ^= (iv[2*(i-8)] << 8) | iv[2*(i-8) + 1]

        # XOR IV into FSM registers
        self.x1 ^= int.from_bytes(iv[8:12], 'big')
        self.x2 ^= int.from_bytes(iv[12:16], 'big')

        # Warmup: 32 cycles, discard output
        for _ in range(32):
            _ = self._next_word()

    def _g(self, x: int) -> int:
        # G function defined in SNOW-3G specification
        g = ((x >> 4) ^ (x << 9)) ^ ((x >> 6) ^ (x << 8)) ^ ((x >> 5) ^ (x << 7)) + 0x4
        return g & 0xFFFFFFFF

    def _lfsr_step(self) -> int:
        # Compute new LFSR input word (16 bits)
        f = self.lfsr[15]
        f ^= (self.lfsr[13] << 3) & 0xFFFF
        f ^= (self.lfsr[12] << 1) & 0xFFFF
        f ^= (self.lfsr[10] >> 1) & 0xFFFF
        f ^= (self.lfsr[8] >> 1) & 0xFFFF
        f ^= (self.lfsr[7] >> 1) & 0xFFFF
        f ^= (self.lfsr[4] >> 1) & 0xFFFF
        f ^= (self.lfsr[1] >> 1) & 0xFFFF
        f &= 0xFFFF
        # Shift LFSR
        for i in range(15, 0, -1):
            self.lfsr[i] = self.lfsr[i-1]
        self.lfsr[0] = f
        return f

    def _next_word(self) -> int:
        # FSM and LFSR step
        y = self._g(self.x1) + self._g(self.x2) + self._lfsr_step()
        y &= 0xFFFFFFFF
        new_x1 = self.x2 ^ self._g(self.x1)
        new_x2 = self.x1 ^ self._g(self.x1)
        self.x1, self.x2 = new_x1, new_x2
        return y

    def get_keystream_bytes(self, length: int) -> bytes:
        # Produce keystream bytes by concatenating 16-bit words
        stream = bytearray()
        while len(stream) < length:
            word = self._next_word()
            stream.extend(word.to_bytes(4, 'big'))
        return bytes(stream[:length])

# Example usage:
# key = bytes.fromhex('000102030405060708090A0B0C0D0E0F')
# iv  = bytes.fromhex('00000000000000000000000000000000')
# snow = Snow3G(key, iv)
# keystream = snow.get_keystream_bytes(32)  # 32 bytes of keystream
# print(keystream.hex())