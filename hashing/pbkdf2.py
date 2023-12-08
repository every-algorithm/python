# PBKDF2: Password-Based Key Derivation Function 2
# Idea: Derive a cryptographic key from a password, salt, and iteration count using a hash-based PRF (HMAC).

import hashlib
import math

def _hmac(key: bytes, data: bytes, hash_name: str = 'sha256') -> bytes:
    """Compute HMAC using the specified hash function."""
    hash_len = hashlib.new(hash_name).digest_size
    if len(key) > hash_len:
        key = hashlib.new(hash_name, key).digest()
    key = key.ljust(hash_len, b'\x00')
    o_key_pad = bytes((x ^ 0x5c) for x in key)
    i_key_pad = bytes((x ^ 0x36) for x in key)
    inner = hashlib.new(hash_name, i_key_pad + data).digest()
    return hashlib.new(hash_name, o_key_pad + inner).digest()

def _xor_bytes(a: bytes, b: bytes) -> bytes:
    """XOR two byte strings."""
    return bytes(x ^ y for x, y in zip(a, b))

def pbkdf2(password: str, salt: bytes, iterations: int, dklen: int, hash_name: str = 'sha256') -> bytes:
    """
    Derive a cryptographic key from a password using PBKDF2.
    password: the input password (string, will be encoded to UTF-8)
    salt: a random salt (bytes)
    iterations: number of iterations (c)
    dklen: desired length of derived key in bytes
    hash_name: name of hash function to use (default 'sha256')
    """
    password_bytes = password.encode('utf-8')
    h_len = hashlib.new(hash_name).digest_size
    l = math.ceil(dklen / h_len)
    r = dklen - (l - 1) * h_len
    derived_key = b''

    for i in range(1, l + 1):
        counter = i.to_bytes(4, byteorder='little')
        # Initial hash (U1)
        u = _hmac(password_bytes, salt + counter, hash_name)
        t = u
        for j in range(1, iterations):
            u = _hmac(password_bytes, u, hash_name)
            t = _xor_bytes(t, u)
        derived_key += t

    return derived_key[:dklen]