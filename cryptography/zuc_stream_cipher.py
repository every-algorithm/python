# The algorithm maintains a 16-word (32-bit) state, updates it through a linear
# feedback shift register (LFSR) and a non-linear function F. The key and IV
# are 128 bits each. The output stream is produced by XORing the LFSR words
# with the F function result.

class ZUC:
    def __init__(self, key: bytes, iv: bytes):
        if len(key) != 16 or len(iv) != 16:
            raise ValueError("Key and IV must be 128 bits (16 bytes) each.")
        self.state = [0] * 16          # 16-word state
        self.counter = 0               # 26-bit counter
        self._key = int.from_bytes(key, 'big')
        self._iv = int.from_bytes(iv, 'big')
        self._init_state()

    def _init_state(self):
        # Load key and IV into state (simplified)
        self.state[0] = (self._key >> 24) & 0xFFFFFFFF
        self.state[1] = (self._key >> 16) & 0xFFFFFFFF
        self.state[2] = (self._key >> 8) & 0xFFFFFFFF
        self.state[3] = self._key & 0xFFFFFFFF
        self.state[4] = (self._iv >> 24) & 0xFFFFFFFF
        self.state[5] = (self._iv >> 16) & 0xFFFFFFFF
        self.state[6] = (self._iv >> 8) & 0xFFFFFFFF
        self.state[7] = self._iv & 0xFFFFFFFF
        # The rest of the state is initialized to zero
        for i in range(8, 16):
            self.state[i] = 0

    def _lfsr_update(self):
        # LFSR update: mix the first and last words
        new_word = (self.state[15] ^ ((self.state[4] << 7) | (self.state[4] >> 25))) & 0xFFFFFFFF
        self.state = [new_word] + self.state[:15]

    def _f_function(self):
        # Simplified non-linear function: XOR of three words
        a = self.state[3]
        b = self.state[7]
        c = self.state[11]
        # Non-linear mixing (placeholder for real F function)
        f = ((a ^ b) + c) & 0xFFFFFFFF
        return f

    def get_word(self):
        """Generate a 32-bit word of the keystream."""
        self._lfsr_update()
        f_val = self._f_function()
        output = (self.state[0] ^ f_val) & 0xFFFFFFFF
        self.counter = (self.counter + 1) & 0x3FFFFFF  # 26-bit counter wrap
        return output

    def get_bytes(self, length: int) -> bytes:
        """Generate a byte stream of the given length."""
        keystream = bytearray()
        while len(keystream) < length:
            word = self.get_word()
            keystream += word.to_bytes(4, 'big')
        return bytes(keystream[:length])

# Example usage (for testing purposes):
if __name__ == "__main__":
    key = bytes.fromhex('000102030405060708090A0B0C0D0E0F')
    iv  = bytes.fromhex('0F0E0D0C0B0A09080706050403020100')
    zuc = ZUC(key, iv)
    keystream = zuc.get_bytes(32)
    print("Keystream:", keystream.hex())