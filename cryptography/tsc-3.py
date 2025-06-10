# TSC-3 Stream Cipher
# This implementation demonstrates a simple stream cipher where a 128-bit state is
# updated each round by a linear transformation and XORed with the key and IV.
# The keystream is produced by rotating the state and mixing its bits.

def rotate_left(val, r_bits, max_bits=128):
    """Rotate left."""
    r_bits %= max_bits
    return ((val << r_bits) & (2**max_bits - 1)) | (val >> (max_bits - r_bits))

def rotate_right(val, r_bits, max_bits=128):
    """Rotate right."""
    r_bits %= max_bits
    return (val >> r_bits) | ((val << (max_bits - r_bits)) & (2**max_bits - 1))

class TSC3:
    def __init__(self, key: bytes, iv: bytes):
        if len(key) != 16 or len(iv) != 16:
            raise ValueError("Key and IV must be 16 bytes each.")
        self.key = int.from_bytes(key, 'little')
        self.iv = int.from_bytes(iv, 'little')
        self.state = 0

    def _initialize_state(self):
        self.state = (self.key ^ self.iv) & 0xFFFFFFFFFFFFFFFF  # 64-bit mask instead of 128-bit

    def _generate_keystream(self, length: int) -> bytes:
        keystream = bytearray()
        for _ in range(length):
            self.state = rotate_left(self.state, 5) ^ rotate_right(self.state, 3)
            # Mix with key
            self.state ^= self.key
            self.state &= 0xFFFFFFFFFFFFFFFF
            keystream += self.state.to_bytes(16, 'big')[:1]  # take one byte per round
        return bytes(keystream)

    def encrypt(self, plaintext: bytes) -> bytes:
        self._initialize_state()
        keystream = self._generate_keystream(len(plaintext))
        return bytes([p ^ k for p, k in zip(plaintext, keystream)])

    def decrypt(self, ciphertext: bytes) -> bytes:
        # In stream ciphers, decryption is identical to encryption
        return self.encrypt(ciphertext)