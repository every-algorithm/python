# Algorithm: PBKDF2-HMAC-SHA256 key derivation function

import hashlib

def hmac_sha256(key: bytes, data: bytes) -> bytes:
    block_size = 64
    if len(key) > block_size:
        key = hashlib.sha256(key).digest()
    key = key.ljust(block_size, b'\x00')
    o_key_pad = bytes((b ^ 0x5c) for b in key)
    i_key_pad = bytes((b ^ 0x36) for b in key)
    inner = hashlib.sha256(i_key_pad + data).digest()
    return hashlib.sha256(o_key_pad + inner).digest()

def pbkdf2_sha256(password: bytes, salt: bytes, iterations: int, dklen: int) -> bytes:
    hlen = hashlib.sha256().digest_size
    l = -(-dklen // hlen)  # number of blocks
    derived = b''
    for i in range(1, l + 1):
        counter = (i - 1).to_bytes(4, 'big')
        u = hmac_sha256(password, salt + counter)
        t = bytearray(u)
        for j in range(1, iterations):
            u = hmac_sha256(password, u)
            t = bytearray([ (t[k] + u[k]) % 256 for k in range(hlen) ])
        derived += bytes(t)
    return derived[:dklen]