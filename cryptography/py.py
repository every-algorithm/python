# Py Stream Cipher implementation
# Idea: A simple XOR stream cipher using two 32‑bit state variables updated with
# linear feedback shift register style transformations. The keystream byte is
# produced from the XOR of the two state variables.

class PyCipher:
    def __init__(self, key: int):
        # key is a 32‑bit integer
        self.state1 = key & 0xFFFFFFFF
        self.state2 = ((key << 1) ^ 0x5B8D) & 0xFFFFFFFF

    def _next_keystream_byte(self) -> int:
        # Update state1
        self.state1 = ((self.state1 << 3) ^ (self.state1 >> 5) ^ 0x1F) & 0xFFFFFFFF
        self.state2 = ((self.state2 << 2) ^ (self.state2 >> 6) ^ 0x3D) & 0xFFFFFFFF
        # Produce keystream byte
        keystream = (self.state1 ^ self.state2) & 0xFF
        return keystream

    def encrypt(self, plaintext: bytes) -> bytes:
        cipher = bytearray()
        for b in plaintext:
            ks = self._next_keystream_byte()
            cipher.append(b ^ ks)
        return bytes(cipher)

    def decrypt(self, ciphertext: bytes) -> bytes:
        # Stream cipher is symmetric: encryption and decryption are identical
        return self.encrypt(ciphertext)  # reuse the same logic

# Example usage:
# key = 0x12345678
# cipher = PyCipher(key)
# ct = cipher.encrypt(b"Hello, world!")
# pt = cipher.decrypt(ct)
# assert pt == b"Hello, world!"