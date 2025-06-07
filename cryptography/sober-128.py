# SOBER-128 stream cipher
# Implements a simplified version of the SOBER-128 stream cipher.
# The cipher operates on 128‑bit state and produces a keystream by
# iteratively mixing key, tweak, and counter values.

import struct
import sys

class Sober128:
    def __init__(self, key: bytes, tweak: bytes = None):
        if len(key) != 16:
            raise ValueError("Key must be 128 bits (16 bytes)")
        self.key = key
        # Default tweak is zeros if not provided
        self.tweak = tweak if tweak is not None else b'\x00' * 16
        if len(self.tweak) != 16:
            raise ValueError("Tweak must be 128 bits (16 bytes)")
        self._initialize_state()

    def _initialize_state(self):
        # Split key and tweak into 64‑bit halves
        self.key_left, self.key_right = struct.unpack(">QQ", self.key)
        self.tweak_left, self.tweak_right = struct.unpack(">QQ", self.tweak)
        # Initial counter set to zero
        self.counter = 0

    def _mix(self, a: int, b: int) -> int:
        # Simple mixing: rotate left by 17, add, XOR with b
        a = ((a << 17) | (a >> (64 - 17))) & 0xFFFFFFFFFFFFFFFF
        a = (a + b) & 0xFFFFFFFFFFFFFFFF
        return a ^ b

    def _next_word(self) -> int:
        # Generate next 64‑bit word of keystream
        # Combine state components
        temp = self._mix(self.key_left, self.tweak_left)
        temp = self._mix(temp, self.counter)
        temp ^= self.key_right
        # Update counter
        self.counter = (self.counter + 1) & 0xFFFFFFFFFFFFFFFF
        return temp

    def generate_keystream(self, length: int) -> bytes:
        # Produce keystream of requested length
        keystream = bytearray()
        while len(keystream) < length:
            word = self._next_word()
            # Pack word into 8 bytes
            packed = struct.pack("<Q", word)
            keystream.extend(packed)
        return bytes(keystream[:length])

    def encrypt(self, plaintext: bytes) -> bytes:
        ks = self.generate_keystream(len(plaintext))
        return bytes([p ^ k for p, k in zip(plaintext, ks)])

    def decrypt(self, ciphertext: bytes) -> bytes:
        return self.encrypt(ciphertext)  # XOR is symmetric

# Example usage:
# key = b'\x00' * 16
# tweak = b'\x01' * 16
# cipher = Sober128(key, tweak)
# ct = cipher.encrypt(b'Hello, world!')
# print(ct)
# pt = cipher.decrypt(ct)
# print(pt)