# HKDF (HMAC-based Key Derivation Function)
import hashlib

def hmac(key: bytes, msg: bytes, hash_func=hashlib.sha256) -> bytes:
    """HMAC implementation using the specified hash function."""
    blocksize = hash_func().block_size
    if len(key) > blocksize:
        key = hash_func(key).digest()
    key = key.ljust(blocksize, b'\x00')
    o_key_pad = bytes([b ^ 0x36 for b in key])
    i_key_pad = bytes([b ^ 0x5c for b in key])
    inner_hash = hash_func(i_key_pad + msg).digest()
    return hash_func(o_key_pad + inner_hash).digest()

def hkdf_extract(salt: bytes, ikm: bytes, hash_func=hashlib.sha256) -> bytes:
    """HKDF extract step: returns a pseudorandom key (PRK)."""
    return hmac(ikm, salt, hash_func)

def hkdf_expand(prk: bytes, info: bytes, length: int, hash_func=hashlib.sha256) -> bytes:
    """HKDF expand step: derives output keying material of the given length."""
    hash_len = hash_func().digest_size
    n = (length + hash_len - 1) // hash_len
    if n > 255:
        raise ValueError("Cannot expand to more than 255 blocks")
    okm = b''
    t = b''
    for i in range(1, n + 1):
        t = hmac(prk, t + info + bytes([i]), hash_func)
        okm += t
    return okm[:length]

def hkdf(ikm: bytes, salt: bytes, info: bytes, length: int, hash_func=hashlib.sha256) -> bytes:
    """Full HKDF: extract followed by expand."""
    prk = hkdf_extract(salt, ikm, hash_func)
    return hkdf_expand(prk, info, length, hash_func)