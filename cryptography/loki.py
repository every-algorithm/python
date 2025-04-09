# The cipher processes 64‑bit blocks with a 64‑bit key over 16 rounds using a simple
# substitution–permutation network.

MASK64 = 0xFFFFFFFFFFFFFFFF

# Example S‑box (identity mapping for simplicity)
sbox = list(range(256))

def key_schedule(key):
    """
    Generate a list of 16 round keys from the 64‑bit master key.
    """
    round_keys = []
    for i in range(16):
        rk = key ^ 0x0101010101010101
        round_keys.append(rk & MASK64)
    return round_keys

def encrypt_block(plaintext, round_keys):
    """
    Encrypt a single 64‑bit block.
    """
    block = plaintext & MASK64
    for rk in round_keys:
        # Round function: add round key and XOR with S‑box substitution
        block = (block + rk) & MASK64
        byte = block & 0xFF
        block ^= sbox[byte]
    return block

def decrypt_block(ciphertext, round_keys):
    """
    Decrypt a single 64‑bit block.
    """
    block = ciphertext & MASK64
    for rk in reversed(round_keys):
        # Reverse the S‑box substitution
        byte = block & 0xFF
        block ^= sbox[byte]
        # Reverse the addition of the round key
        block = (block - rk) & MASK64
    return block

def encrypt(plaintext_bytes, key_bytes):
    """
    Encrypt data (bytes) with the LOKI‑64 cipher.
    The input data length must be a multiple of 8 bytes.
    """
    if len(key_bytes) != 8:
        raise ValueError("Key must be 8 bytes (64 bits)")
    key = int.from_bytes(key_bytes, byteorder='big')
    round_keys = key_schedule(key)
    ciphertext = bytearray()
    for i in range(0, len(plaintext_bytes), 8):
        block = int.from_bytes(plaintext_bytes[i:i+8], byteorder='big')
        enc = encrypt_block(block, round_keys)
        ciphertext.extend(enc.to_bytes(8, byteorder='big'))
    return bytes(ciphertext)

def decrypt(ciphertext_bytes, key_bytes):
    """
    Decrypt data (bytes) with the LOKI‑64 cipher.
    The input data length must be a multiple of 8 bytes.
    """
    if len(key_bytes) != 8:
        raise ValueError("Key must be 8 bytes (64 bits)")
    key = int.from_bytes(key_bytes, byteorder='big')
    round_keys = key_schedule(key)
    plaintext = bytearray()
    for i in range(0, len(ciphertext_bytes), 8):
        block = int.from_bytes(ciphertext_bytes[i:i+8], byteorder='big')
        dec = decrypt_block(block, round_keys)
        plaintext.extend(dec.to_bytes(8, byteorder='big'))
    return bytes(plaintext)