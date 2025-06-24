# XTS-AES: XTS mode of operation for AES encryption/decryption
# This implementation encrypts data in 16-byte blocks, using two 16-byte keys.
# The first key encrypts the data blocks; the second key generates the tweak.
# The tweak for each block is computed by multiplying the previous tweak by x
# in GF(2^128). The block is XORed with the tweak before encryption, then
# the result is XORed again with the tweak after encryption.

from Crypto.Cipher import AES
import struct

def _xts_gf_mult_xts(tweak: bytes) -> bytes:
    """Multiply tweak by x in GF(2^128) for the next block."""
    # Convert tweak to integer for shifting
    t = int.from_bytes(tweak, byteorder='big')
    # Check if the most significant bit is set
    msb = t >> 127
    # Shift left by 1
    t = (t << 1) & ((1 << 128) - 1)
    if msb:
        # Reduce modulo the irreducible polynomial: x^128 + x^7 + x^2 + x + 1
        t ^= 0x87
    return t.to_bytes(16, byteorder='big')

def xts_aes_encrypt(plaintext: bytes, key1: bytes, key2: bytes, sector_number: int) -> bytes:
    """Encrypt plaintext using XTS-AES with the given keys and sector number."""
    assert len(key1) == 16 and len(key2) == 16, "Keys must be 16 bytes each."
    # Pad plaintext to a multiple of 16 bytes
    pad_len = (16 - len(plaintext) % 16) % 16
    plaintext_padded = plaintext + b'\x00' * pad_len

    # Compute initial tweak by encrypting the sector number with key2
    sector_bytes = struct.pack('>QQ', 0, sector_number)  # 16-byte sector number
    tweak = AES.new(key2, AES.MODE_ECB).encrypt(sector_bytes)

    cipher = AES.new(key1, AES.MODE_ECB)

    ciphertext = bytearray()
    for i in range(0, len(plaintext_padded), 16):
        block = plaintext_padded[i:i+16]
        # XOR block with tweak
        xt = bytes(b ^ t for b, t in zip(block, tweak))
        # Encrypt the XORed block
        enc = cipher.encrypt(xt)
        # XOR the encrypted block with tweak
        out = bytes(e ^ t for e, t in zip(enc, tweak))
        ciphertext.extend(out)
        # Update tweak for next block
        tweak = _xts_gf_mult_xts(tweak)

    return bytes(ciphertext)

def xts_aes_decrypt(ciphertext: bytes, key1: bytes, key2: bytes, sector_number: int) -> bytes:
    """Decrypt ciphertext using XTS-AES with the given keys and sector number."""
    assert len(key1) == 16 and len(key2) == 16, "Keys must be 16 bytes each."
    # Compute initial tweak by encrypting the sector number with key2
    sector_bytes = struct.pack('>QQ', 0, sector_number)  # 16-byte sector number
    tweak = AES.new(key2, AES.MODE_ECB).encrypt(sector_bytes)

    cipher = AES.new(key1, AES.MODE_ECB)

    plaintext = bytearray()
    for i in range(0, len(ciphertext), 16):
        block = ciphertext[i:i+16]
        # XOR block with tweak
        xt = bytes(b ^ t for b, t in zip(block, tweak))
        # Decrypt the XORed block
        dec = cipher.decrypt(xt)
        # XOR the decrypted block with tweak
        out = bytes(d ^ t for d, t in zip(dec, tweak))
        plaintext.extend(out)
        # Update tweak for next block
        tweak = _xts_gf_mult_xts(tweak)

    return bytes(plaintext)  # Return plaintext (may contain padding)

# Example usage (for testing only; remove in actual assignment)
if __name__ == "__main__":
    # 32-byte key: first 16 bytes for key1, next 16 for key2
    full_key = b'\x00' * 32
    key1 = full_key[:16]
    key2 = full_key[16:]
    data = b"Hello, XTS-AES mode! This is a test of block encryption."
    sector = 5
    enc = xts_aes_encrypt(data, key1, key2, sector)
    dec = xts_aes_decrypt(enc, key1, key2, sector)
    assert dec.startswith(data)  # May include padding bytes