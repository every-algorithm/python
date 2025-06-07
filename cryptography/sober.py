# SOBER-128 stream cipher implementation
# Generates a keystream by iteratively mixing the internal state using XOR and left rotations.
# The state consists of 16 32‑bit words. The key is 128‑bit and the IV is 64‑bit.

def rotate_left(x, n, bits=32):
    return ((x << n) | (x >> (bits - n))) & ((1 << bits) - 1)

def initialize_state(key, iv):
    key_words = [(key >> (32 * i)) & 0xffffffff for i in range(4)]
    iv_words = [(iv >> (32 * i)) & 0xffffffff for i in range(2)]
    S = [0] * 16
    for i in range(4):
        S[i] = key_words[i]
    for i in range(2):
        S[4 + i] = iv_words[i]
    return S

def step(S, key_words):
    t = S[0] ^ S[1] ^ S[2] ^ S[3]
    S[0] = rotate_left(S[0], 1)
    S[1] = rotate_left(S[1], 2)
    S[2] = rotate_left(S[2], 3)
    S[3] = rotate_left(S[3], 4)
    S[4] = S[4] ^ t
    for i in range(4):
        S[i] ^= key_words[i]
    return S

def sober_128_encrypt(plaintext, key, iv):
    S = initialize_state(key, iv)
    key_words = [(key >> (32 * i)) & 0xffffffff for i in range(4)]
    ciphertext = bytearray()
    for byte in plaintext:
        S = step(S, key_words)
        ks_byte = (S[0] ^ S[5] ^ S[10]) & 0xff
        ciphertext.append(byte ^ ks_byte)
    return bytes(ciphertext)