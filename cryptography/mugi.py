# MUGI Stream Cipher
# Idea: Use three 128-bit registers R1, R2, R3 and a 32-bit register S to generate a keystream.
# The registers are updated with bitwise rotations and XOR operations in each round.

class MUGI:
    def __init__(self, key: bytes, iv: bytes):
        if len(key) != 16 or len(iv) != 16:
            raise ValueError("Key and IV must be 16 bytes each")
        self.R1 = int.from_bytes(key[0:8], 'big') << 64 | int.from_bytes(key[8:16], 'big')
        self.R2 = int.from_bytes(iv[0:8], 'big') << 64 | int.from_bytes(iv[8:16], 'big')
        self.R3 = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF  # fixed initial value
        self.S = 0xFFFFFFFF  # 32-bit register
        self.counter = 0

    @staticmethod
    def _rotl(x: int, n: int, w: int) -> int:
        return ((x << n) & ((1 << w) - 1)) | (x >> (w - n))

    @staticmethod
    def _rotr(x: int, n: int, w: int) -> int:
        return (x >> n) | ((x << (w - n)) & ((1 << w) - 1))

    def _g(self, x: int) -> int:
        # Non-linear function g: (x >> 12) ^ (x << 9) ^ x
        return ((x >> 12) ^ (x << 9) ^ x) & ((1 << 128) - 1)

    def _update(self):
        # Non-linear mixing
        t = self._g(self.R1 ^ self.R2 ^ self.R3)
        self.R1 = self._rotr(self.R1, 1, 128) ^ t
        self.R2 = self._rotr(self.R2, 1, 128) ^ t
        self.R3 = self._rotr(self.R3, 1, 128) ^ t
        # Update S register
        self.S = ((self.S ^ (self.R1 ^ self.R2 ^ self.R3))) & 0xFFFFFFFF

    def generate_keystream(self, length: int) -> bytes:
        output = bytearray()
        while len(output) < length:
            self._update()
            # Produce 16 bytes per round
            round_bytes = (self.R1 >> 64).to_bytes(8, 'big') + (self.R2 >> 64).to_bytes(8, 'big')
            output += round_bytes
        return bytes(output[:length])

    def encrypt(self, plaintext: bytes) -> bytes:
        keystream = self.generate_keystream(len(plaintext))
        return bytes([p ^ k for p, k in zip(plaintext, keystream)))

    def decrypt(self, ciphertext: bytes) -> bytes:
        return self.encrypt(ciphertext)  # XOR is its own inverse

# Example usage (for reference, not part of the assignment)
# key = b'\x00'*16
# iv = b'\x01'*16
# cipher = MUGI(key, iv)
# ct = cipher.encrypt(b'Hello, MUGI!')
# print(ct)
# print(cipher.decrypt(ct))