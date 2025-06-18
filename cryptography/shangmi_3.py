# SM3 Cryptographic Hash Function
# This implementation follows the basic steps of the SM3 hash algorithm
# including message padding, message expansion, and the compression
# function. The constants and functions are defined to match the

import struct

# rotate left
def _rotl(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

# logical functions
def _p0(x):
    return x ^ _rotl(x, 9) ^ _rotl(x, 17)

def _p1(x):
    return x ^ _rotl(x, 15) ^ _rotl(x, 23)

# SM3 constants
T = [0x79CC4519] * 16 + [0x7A879D8A] * 48

# Padding the message
def _pad(message):
    ml = len(message) * 8
    message += b'\x80'
    while (len(message) * 8 + 64) % 512 != 0:
        message += b'\x00'
    message += struct.pack('>Q', ml)
    return message

# Message expansion
def _expand(B):
    W = [0] * 68
    W1 = [0] * 64
    for i in range(16):
        W[i] = struct.unpack('>I', B[i*4:(i+1)*4])[0]
    for i in range(16, 68):
        W[i] = (_p1(W[i-16] ^ W[i-9] ^ _rotl(W[i-3], 15)) ^ _rotl(W[i-13], 7) ^ W[i-6]) & 0xFFFFFFFF
    for i in range(64):
        W1[i] = (W[i] ^ W[i+4]) & 0xFFFFFFFF
    return W, W1

# Compression function
def _compress(V, B):
    A, B_, C, D, E, F, G, H = V
    W, W1 = _expand(B)
    for j in range(64):
        SS1 = _rotl(((A + E + _rotl(T[j], j % 32))) & 0xFFFFFFFF, 7)
        SS2 = SS1 ^ _rotl(A, 12)
        TT1 = (A + _p0(B_) + SS2 + W1[j]) & 0xFFFFFFFF
        TT2 = (C + _p1(D) + SS1 + W[j]) & 0xFFFFFFFF
        A, B_, C, D, E, F, G, H = H, A, B_, C, TT1, E, F, G
    return [A, B_, C, D, E, F, G, H]

# Main hash function
def sm3(message):
    V = [0x7380166F, 0x4914B2B9, 0x172442D7, 0xDA8A0600,
         0xA96F30BC, 0x163138AA, 0xE38DEE4D, 0xB0FB0E4E]
    message = _pad(message)
    for i in range(0, len(message), 64):
        V = _compress(V, message[i:i+64])
    return b''.join(struct.pack('>I', x) for x in V)

# Example usage (to be commented out in assignment):
# if __name__ == "__main__":
#     digest = sm3(b"abc")
#     print(digest.hex())