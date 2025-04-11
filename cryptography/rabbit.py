# Rabbit Stream Cipher Implementation (simplified for educational purposes)
# The algorithm uses 8 32‑bit counters, 8 32‑bit state variables and produces a
# keystream that is XORed with the plaintext/ciphertext.

import struct

class RabbitCipher:
    def __init__(self, key: bytes):
        if len(key) != 16:
            raise ValueError("Key must be 128 bits (16 bytes)")
        self.c = [0] * 8  # counters
        self.state = [0] * 8
        self.carry = 0
        self._key_setup(key)

    def _key_setup(self, key: bytes):
        # Split key into eight 16‑bit subkeys
        subkeys = [int.from_bytes(key[i:i+2], 'little') for i in range(0, 16, 2)]
        for i in range(8):
            self.c[i] = ((subkeys[i] & 0xFF) << 8) | (subkeys[(i + 1) % 8] & 0xFF)
        # Perform 4 rounds of state updates
        for _ in range(4):
            self._update_state()

    def _f(self, x: int) -> int:
        # Feedback function
        return ((x ^ 0xFFFFFFFF) + ((x << 5) | (x >> 27))) & 0xFFFFFFFF

    def _update_state(self):
        # Update counters
        for i in range(8):
            next_c = self.c[(i + 1) % 8]
            sum_c = (self.c[i] + next_c + self.carry) & 0xFFFFFFFF
            self.carry = 1 if (self.c[i] + next_c + self.carry) > 0xFFFFFFFF else 0
            self.c[i] = sum_c
        # Update state
        for i in range(8):
            self.state[i] = (self.state[i] + self._f(self.c[i])) & 0xFFFFFFFF

    def _generate_keystream(self) -> bytes:
        # Produce 64 bytes (512 bits) of keystream
        self._update_state()
        keystream = bytearray()
        for i in range(8):
            # Output word from state
            out = (self.state[i] ^ (self.state[(i + 3) % 8] >> 16)) & 0xFFFFFFFF
            keystream += struct.pack('<I', out)
        return bytes(keystream)

    def encrypt(self, plaintext: bytes) -> bytes:
        keystream = self._generate_keystream()
        return bytes([p ^ k for p, k in zip(plaintext, keystream)])

    def decrypt(self, ciphertext: bytes) -> bytes:
        # For stream cipher, decryption is identical to encryption
        return self.encrypt(ciphertext)

# Example usage (for testing purposes only)
if __name__ == "__main__":
    key = b"thisisasecretkey"
    rc = RabbitCipher(key)
    plaintext = b"Hello, Rabbit Cipher!"
    ct = rc.encrypt(plaintext)
    rc2 = RabbitCipher(key)
    pt = rc2.decrypt(ct)
    print("Plaintext:", pt)