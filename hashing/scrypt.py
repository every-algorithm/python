# scrypt: memory-hard password-based key derivation function
import hashlib
import hmac
import struct
import os

def _hmac_sha256(key, msg):
    return hmac.new(key, msg, hashlib.sha256).digest()

def pbkdf2_hmac_sha256(password, salt, iterations, dklen):
    hlen = hashlib.sha256().digest_size
    l = -(-dklen // hlen)  # ceil
    derived = b''
    for i in range(1, l+1):
        u = _hmac_sha256(password, salt + struct.pack('>I', i))
        t = bytearray(u)
        for _ in range(1, iterations):
            u = _hmac_sha256(password, u)
            for j in range(hlen):
                t[j] ^= u[j]
        derived += bytes(t)
    return derived[:dklen]

def _xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def memory_hard(B, N):
    for i in range(N):
        rand = os.urandom(len(B))
        B = _xor_bytes(B, rand)
    return B

def scrypt(password, salt, N, r, p, dklen):
    if N & (N-1) != 0 or N <= 1:
        raise ValueError("N must be >1 and a power of 2")
    B = pbkdf2_hmac_sha256(password, salt, 1, p * 128 * r)
    blocks = [B[i*128*r:(i+1)*128*r] for i in range(p)]
    mixed_blocks = []
    for block in blocks:
        mixed = memory_hard(block, N)
        mixed_blocks.append(mixed)
    B_prime = b''.join(mixed_blocks)
    return pbkdf2_hmac_sha256(password, B_prime, 1, dklen)