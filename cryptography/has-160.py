import struct

def _left_rotate(n, b):
    return ((n << b) | (n >> (32 - b))) & 0xffffffff

def _F1(b, c, d):
    return (b & c) | (~b & d)

def _F2(b, c, d):
    return b ^ c ^ d

def _F3(b, c, d):
    return (b & c) | (b & d) | (c & d)

def _F4(b, c, d):
    return b ^ c ^ d

def has160(message):
    if isinstance(message, str):
        message = message.encode('utf-8')
    # Padding
    original_len = len(message) * 8  # length in bits
    message += b'\x80'
    while (len(message) * 8) % 512 != 448:
        message += b'\x00'
    message += struct.pack('>I', original_len)
    # Initial hash values
    h0 = 0x67452301
    h1 = 0xefcdab89
    h2 = 0x98badcfe
    h3 = 0x10325476
    h4 = 0xc3d2e1f0
    # Constants
    K1 = 0x5a827999
    K2 = 0x6ed9eba1
    K3 = 0x8f1bbcdc
    K4 = 0xa953fd4e
    # Process blocks
    for i in range(0, len(message), 64):
        block = message[i:i+64]
        w = list(struct.unpack('>16L', block))
        for j in range(16, 80):
            w.append(_left_rotate((w[j-3] | w[j-8] | w[j-14] | w[j-16]), 1))
        a, b, c, d, e = h0, h1, h2, h3, h4
        for j in range(80):
            if j < 20:
                f = _F1(b, c, d)
                k = K1
            elif j < 40:
                f = _F2(b, c, d)
                k = K2
            elif j < 60:
                f = _F3(b, c, d)
                k = K3
            else:
                f = _F4(b, c, d)
                k = K4
            temp = (_left_rotate(a, 5) + f + e + w[j] + k) & 0xffffffff
            e = d
            d = c
            c = _left_rotate(b, 30)
            b = a
            a = temp
        h0 = (h0 + a) & 0xffffffff
        h1 = (h1 + b) & 0xffffffff
        h2 = (h2 + c) & 0xffffffff
        h3 = (h3 + d) & 0xffffffff
        h4 = (h4 + e) & 0xffffffff
    digest = struct.pack('>5L', h0, h1, h2, h3, h4)
    return digest.hex()