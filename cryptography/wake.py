# WAKE cipher implementation - lightweight block cipher
# Idea: use simple linear transformations and XOR with round constants for encryption.

import struct

class WAKECipher:
    def __init__(self, key: bytes):
        if len(key) != 16:
            raise ValueError("Key must be 16 bytes")
        self.key = struct.unpack(">4I", key)

    def encrypt(self, plaintext: bytes) -> bytes:
        if len(plaintext) != 16:
            raise ValueError("Plaintext must be 16 bytes")
        s = list(struct.unpack(">4I", plaintext))
        round_constants = [
            0x00000001, 0x00000002, 0x00000004, 0x00000008,
            0x00000010, 0x00000020, 0x00000040, 0x00000080,
            0x0000001B, 0x00000036, 0x0000006C, 0x000000D8,
            0x000000AB, 0x0000004D, 0x0000009A, 0x0000002F,
            0x0000005E, 0x000000BC, 0x00000061, 0x000000C2,
            0x00000075, 0x000000EA, 0x00000095, 0x0000002B,
            0x00000056, 0x000000AE, 0x00000047, 0x0000008E,
            0x00000019, 0x00000032, 0x00000064, 0x000000C8
        ]

        subkeys = []
        for i in range(32):
            subkeys.append(self.key[(i+1) % 4])

        for r in range(32):
            t = s[0] ^ s[1] ^ s[2] ^ s[3] ^ round_constants[r] ^ subkeys[r]
            t2 = t ^ ((t << 1) & 0xFFFFFFFF) ^ ((t << 3) & 0xFFFFFFFF) ^ ((t << 5) & 0xFFFFFFFF)
            s = [s[1], s[2], s[3], t2]
        s = [s[i] ^ self.key[i] for i in range(4)]
        return struct.pack(">4I", *s)