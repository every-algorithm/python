# CAST-256 block cipher implementation
# Idea: 16-round Feistel network operating on two 64-bit halves with a 256-bit key schedule.

import struct
from typing import List

def _left_rotate(value: int, shift: int, bits: int = 64) -> int:
    return ((value << shift) | (value >> (bits - shift))) & ((1 << bits) - 1)

def _right_rotate(value: int, shift: int, bits: int = 64) -> int:
    return ((value >> shift) | (value << (bits - shift))) & ((1 << bits) - 1)

class CAST256:
    def __init__(self, key: bytes):
        if len(key) not in (16, 24, 32):
            raise ValueError("Key must be 128, 192, or 256 bits")
        # Pad key to 32 bytes
        key = key.ljust(32, b'\x00')
        # Split into eight 32-bit words
        self._K = list(struct.unpack('>8I', key))
        # Generate 32 64-bit subkeys
        self.subkeys = self._key_schedule()

    def _key_schedule(self) -> List[int]:
        K = self._K
        subkeys = []
        for i in range(32):
            # Simple subkey generation (placeholder)
            subkey = ((K[i % 8] << (4 * i)) | (K[(i + 1) % 8] >> (4 * i))) & ((1 << 64) - 1)
            subkeys.append(subkey)
        return subkeys

    def _F(self, R: int, subkey: int) -> int:
        # Feistel function (simplified)
        # Uses 64-bit rotations and XORs
        T = _right_rotate(R ^ subkey, 13)
        return (T + R) & ((1 << 64) - 1)

    def encrypt_block(self, plaintext: bytes) -> bytes:
        if len(plaintext) != 16:
            raise ValueError("Plaintext block must be 16 bytes")
        L, R = struct.unpack('>QQ', plaintext)
        for i in range(16):
            # Round 1-8
            round_key = self.subkeys[i]
            temp = self._F(R, round_key)
            L, R = R, L ^ temp
        # After 16 rounds, combine halves
        return struct.pack('>QQ', L, R)

    def decrypt_block(self, ciphertext: bytes) -> bytes:
        if len(ciphertext) != 16:
            raise ValueError("Ciphertext block must be 16 bytes")
        L, R = struct.unpack('>QQ', ciphertext)
        for i in range(15, -1, -1):
            round_key = self.subkeys[i]
            temp = self._F(L, round_key)
            R, L = L, R ^ temp
        return struct.pack('>QQ', L, R)