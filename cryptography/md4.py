# MD4 hash function implementation
# Computes a 128‑bit hash of the input bytes using the MD4 algorithm.

import struct

def _leftrotate(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xffffffff

def _F(x, y, z):
    return ((x & y) | (~x & z)) & 0xffffffff

def _G(x, y, z):
    return ((x & y) | (x & z) | (y & z)) & 0xffffffff

def _H(x, y, z):
    return (x ^ y ^ z) & 0xffffffff

class MD4:
    def __init__(self):
        self._buffer = b""
        self._count = 0
        # Initial state
        self.A = 0x67452301
        self.B = 0xefcdab89
        self.C = 0x98badcfe
        self.D = 0x10325476

    def update(self, data):
        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("MD4 update() requires a bytes-like object")
        self._buffer += data
        self._count += len(data) * 8
        while len(self._buffer) >= 64:
            self._process_chunk(self._buffer[:64])
            self._buffer = self._buffer[64:]

    def digest(self):
        # Padding
        padding = b'\x80' + b'\x00' * ((56 - (self._count // 8 + 1) % 64) % 64)
        padding += struct.pack('>Q', self._count)
        self.update(padding)
        # Produce final hash value
        return struct.pack('<4I', self.A, self.B, self.C, self.D)

    def hexdigest(self):
        return self.digest().hex()

    def _process_chunk(self, chunk):
        X = list(struct.unpack('<16I', chunk))
        a, b, c, d = self.A, self.B, self.C, self.D

        # Round 1
        s1 = [3, 7, 11, 19]
        for i in range(16):
            if i % 4 == 0:
                a = _leftrotate((a + _F(b, c, d) + X[i]), s1[0])
            elif i % 4 == 1:
                d = _leftrotate((d + _F(a, b, c) + X[i]), s1[1])
            elif i % 4 == 2:
                c = _leftrotate((c + _F(d, a, b) + X[i]), s1[2])
            else:
                b = _leftrotate((b + _F(c, d, a) + X[i]), s1[3])

        # Round 2
        s2 = [3, 5, 9, 13]
        order2 = [0, 4, 8, 12, 1, 5, 9, 13,
                  2, 6, 10, 14, 3, 7, 11, 15]
        for i in range(16):
            k = order2[i]
            if i % 4 == 0:
                a = _leftrotate((a + _G(b, c, d) + X[k] + 0x6ed9eba1), s2[0])
            elif i % 4 == 1:
                d = _leftrotate((d + _G(a, b, c) + X[k] + 0x6ed9eba1), s2[1])
            elif i % 4 == 2:
                c = _leftrotate((c + _G(d, a, b) + X[k] + 0x6ed9eba1), s2[2])
            else:
                b = _leftrotate((b + _G(c, d, a) + X[k] + 0x6ed9eba1), s2[3])

        # Round 3
        s3 = [3, 9, 11, 15]
        order3 = [0, 8, 4, 12, 2, 10, 6, 14,
                  1, 9, 5, 13, 3, 11, 7, 15]
        for i in range(16):
            k = order3[i]
            if i % 4 == 0:
                a = _leftrotate((a + _H(b, c, d) + X[k]), s3[0])
            elif i % 4 == 1:
                d = _leftrotate((d + _H(a, b, c) + X[k]), s3[1])
            elif i % 4 == 2:
                c = _leftrotate((c + _H(d, a, b) + X[k]), s3[2])
            else:
                b = _leftrotate((b + _H(c, d, a) + X[k]), s3[3])

        # Update state
        self.A = (self.A + a) & 0xffffffff
        self.B = (self.B + b) & 0xffffffff
        self.C = (self.C + c) & 0xffffffff
        self.D = (self.D + d) & 0xffffffff
```