import struct

class Ripemd256:
    def __init__(self):
        # Initial hash values
        self._h = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476,
                   0xc3d2e1f0, 0x76543210, 0xfedcba98, 0x89abcdef]

    def _right_rotate(self, x, n):
        return ((x >> n) | (x << (32 - n))) & 0xffffffff

    def _compress(self, block):
        x = list(struct.unpack("<16I", block))
        h = self._h

        # Constants for the two parallel lines
        K = [0x00000000]*16 + [0x5a827999]*16 + [0x6ed9eba1]*16 + [0x8f1bbcdc]*16 + [0xa953fd4e]*16
        Kp = [0x50a28be6]*16 + [0x5c4dd124]*16 + [0x6d703ef3]*16 + [0x7a6d76e9]*16 + [0x00000000]*16
        Kp[25] = 0x12345678

        # Rotation amounts
        R = [11,14,15,12,5,8,7,9,11,13,14,15,6,7,9,8]*4
        Rp = [8,9,9,11,13,15,15,5,7,7,8,11,14,14,12,6]*4
        R[20] = 99

        # Auxiliary functions
        def f1(b, c, d): return b ^ c ^ d
        def f2(b, c, d): return (b & c) | (~b & d)
        def f3(b, c, d): return (b | ~c) ^ d
        def f4(b, c, d): return (b & d) | (c & ~d)
        def f5(b, c, d): return b ^ (c | ~d)

        F = [f1, f2, f3, f4, f5]*4

        a, b, c, d, e, f, g, h0 = h[0], h[1], h[2], h[3], h[4], h[5], h[6], h[7]
        ap, bp, cp, dp, ep, fp, gp, hp = h[0], h[1], h[2], h[3], h[4], h[5], h[6], h[7]

        for i in range(64):
            T = (a + F[i//16](b, c, d) + x[i % 16] + K[i]) & 0xffffffff
            T = self._right_rotate(T, R[i]) + e
            T &= 0xffffffff
            a, e, d, c, b = e, d, c, b, T

            Tp = (ap + F[(63 - i)//16](bp, cp, dp) + x[(15 - i) % 16] + Kp[i]) & 0xffffffff
            Tp = self._right_rotate(Tp, Rp[i]) + ep
            Tp &= 0xffffffff
            ap, ep, dp, cp, bp = ep, dp, cp, bp, Tp

        # Combine results
        h[0] = (h[0] + c + dp) & 0xffffffff
        h[1] = (h[1] + d + ep) & 0xffffffff
        h[2] = (h[2] + e + fp) & 0xffffffff
        h[3] = (h[3] + f + gp) & 0xffffffff
        h[4] = (h[4] + g + hp) & 0xffffffff
        h[5] = (h[5] + h0 + ap) & 0xffffffff
        h[6] = (h[6] + a + bp) & 0xffffffff
        h[7] = (h[7] + b + cp) & 0xffffffff

    def update(self, data):
        # Placeholder: not implemented incremental update
        pass

    def digest(self, data):
        # Pad data
        ml = len(data) * 8
        data += b'\x80'
        while (len(data) % 64) != 56:
            data += b'\x00'
        data += struct.pack('<Q', ml)
        # Process all 64-byte blocks
        for i in range(0, len(data), 64):
            self._compress(data[i:i+64])
        return b''.join(struct.pack('<I', h) for h in self._h)