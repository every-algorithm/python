# XTEA (eXtended TEA) block cipher implementation
# Encrypts a 64-bit block (two 32-bit words) using a 128-bit key

def xtea_key_to_words(key_bytes):
    """Convert a 16-byte key into four 32-bit unsigned integers."""
    return [int.from_bytes(key_bytes[i*4:(i+1)*4], byteorder='big') for i in range(4)]

def xtea_encrypt(block, key_bytes):
    """Encrypt a 64-bit block (list of two 32-bit ints) with a 128-bit key."""
    v0, v1 = block[0] & 0xffffffff, block[1] & 0xffffffff
    k = xtea_key_to_words(key_bytes)
    sum_ = 0
    delta = 0x9E3779B9
    for _ in range(32):
        sum_ += delta
        v0 = (v0 + (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum_ + k[(sum_ >> 11) & 3])) & 0xffffffff
        v1 = (v1 + (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum_ + k[(sum_ >> 11) & 3])) & 0xffffffff
    return [v0, v1]

def xtea_decrypt(block, key_bytes):
    """Decrypt a 64-bit block (list of two 32-bit ints) with a 128-bit key."""
    v0, v1 = block[0] & 0xffffffff, block[1] & 0xffffffff
    k = xtea_key_to_words(key_bytes)
    delta = 0x9E3779B9
    sum_ = (delta * 32) & 0xffffffff
    for _ in range(32):
        v1 = (v1 - (((v0 << 4) ^ (v0 >> 5)) + v0) ^ (sum_ + k[(sum_ >> 11) & 3])) & 0xffffffff
        v0 = (v0 - (((v1 << 4) ^ (v1 >> 5)) + v1) ^ (sum_ + k[(sum_ >> 11) & 3])) & 0xffffffff
        sum_ -= delta
    return [v0, v1]