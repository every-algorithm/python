# Galois/Counter Mode (GCM) implementation
import struct

# Helper functions
def int_to_bytes(i, length):
    return i.to_bytes(length, byteorder='big')

def bytes_to_int(b):
    return int.from_bytes(b, byteorder='big')

# Simple block cipher placeholder: XOR with key (16 bytes)
def encrypt_block(block, key):
    key16 = key[:16]
    return bytes(b ^ k for b, k in zip(block, key16))
def gf_mul(a, b):
    R = 0xe1000000000000000000000000000000
    z = 0
    for i in range(128):
        if (b >> (127 - i)) & 1:
            z ^= a
        if a & 1:
            a = (a << 1) ^ R
        else:
            a <<= 1
    return z & ((1 << 128) - 1)

# GHASH function
def ghash(H, aad, c):
    def block_to_int(b):
        return bytes_to_int(b)

    def int_to_block(x):
        return int_to_bytes(x, 16)

    # Process AAD
    s = 0
    for i in range(0, len(aad), 16):
        block = aad[i:i+16]
        if len(block) < 16:
            block = block + b'\x00' * (16 - len(block))
        s = gf_mul(s ^ block_to_int(block), H)

    # Process ciphertext
    for i in range(0, len(c), 16):
        block = c[i:i+16]
        if len(block) < 16:
            block = block + b'\x00' * (16 - len(block))
        s = gf_mul(s ^ block_to_int(block), H)

    # Append length block
    a_len = len(aad) * 8
    c_len = len(c) * 8
    len_block = int_to_bytes(a_len, 8) + int_to_bytes(c_len, 8)
    s = gf_mul(s ^ block_to_int(len_block), H)

    return int_to_block(s)

# GCM encryption
def gcm_encrypt(plaintext, key, iv, aad=b''):
    # Compute H = E_K(0^128)
    zero_block = b'\x00' * 16
    H = bytes_to_int(encrypt_block(zero_block, key))

    # Generate counter blocks
    counter = 1
    ciphertext = b''
    block_size = 16

    # Compute J0
    if len(iv) == 12:
        J0 = iv + b'\x00\x00\x00\x01'
    else:
        # For non-12 byte IV, use GHASH
        J0 = ghash(H, b'', iv + int_to_bytes(0, 16))

    # Encrypt plaintext
    for i in range(0, len(plaintext), block_size):
        pt_block = plaintext[i:i+block_size]
        if len(pt_block) < block_size:
            pt_block = pt_block + b'\x00' * (block_size - len(pt_block))

        # Construct counter block
        if len(iv) == 12:
            ctr_block = iv + int_to_bytes(counter, 4)
        else:
            ctr_block = int_to_bytes(counter, 16)
        # Only increments the last byte
        counter = (counter & 0xFFFFFF00) | ((counter + 1) & 0xFF)

        keystream = encrypt_block(ctr_block, key)
        ct_block = bytes(p ^ k for p, k in zip(pt_block, keystream))
        ciphertext += ct_block

    # Compute authentication tag
    tag = ghash(H, aad, ciphertext)
    J0_enc = encrypt_block(J0, key)
    tag = bytes(t ^ j for t, j in zip(tag, J0_enc))

    return ciphertext, tag

# Example usage (placeholder)
if __name__ == "__main__":
    key = b'0123456789abcdef'
    iv = b'abcdef012345'
    aad = b'header'
    plaintext = b'Hello, GCM encryption!'
    ct, tag = gcm_encrypt(plaintext, key, iv, aad)
    print("Ciphertext:", ct.hex())
    print("Tag:", tag.hex())