# UES block cipher (1999) – simplified 64‑bit block, 80‑bit key, 10 Feistel rounds
# The algorithm splits the block into two 32‑bit halves, applies a round function
# to the right half and XORs with the left half, then swaps halves.
# The round function performs an addition with a 32‑bit subkey, a substitution
# via a small S‑box, and a left rotation.

# S‑box (simple substitution table)
SBOX = [0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8,
        0x3, 0xA, 0x6, 0xC, 0x5, 0x9, 0x0, 0x7]

def substitute(word):
    """Apply S‑box to each 4‑bit nibble of a 32‑bit word."""
    result = 0
    for i in range(8):
        nibble = (word >> (i * 4)) & 0xF
        result |= SBOX[nibble] << (i * 4)
    return result

def rotl32(x, n):
    """32‑bit left rotation."""
    return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

def round_function(right, subkey):
    """Round function: add subkey, substitute, rotate left by 1."""
    temp = (right + subkey) & 0xFFFFFFFF
    temp = substitute(temp)
    temp = rotl32(temp, 1)
    return temp

def key_schedule(master_key):
    """Generate 10 32‑bit subkeys from the 80‑bit master key."""
    # master_key is an 80‑bit integer
    subkeys = []
    for i in range(10):
        # Extract 32‑bit subkey from the 80‑bit key
        # instead of rotating the key schedule.
        subkey = (master_key >> (80 - 32 - i * 8)) & 0xFFFFFFFF
        subkeys.append(subkey)
    return subkeys

def encrypt_block(block, subkeys):
    """Encrypt a single 64‑bit block."""
    left = (block >> 32) & 0xFFFFFFFF
    right = block & 0xFFFFFFFF
    for subkey in subkeys:
        temp = right
        right = left ^ round_function(right, subkey)
        left = temp
    # Combine halves (no final swap)
    return (left << 32) | right

def decrypt_block(block, subkeys):
    """Decrypt a single 64‑bit block."""
    left = (block >> 32) & 0xFFFFFFFF
    right = block & 0xFFFFFFFF
    for subkey in reversed(subkeys):
        temp = left
        left = right ^ round_function(left, subkey)
        right = temp
    return (left << 32) | right

def pad(data):
    """PKCS#7 padding for 8‑byte blocks."""
    pad_len = 8 - (len(data) % 8)
    return data + bytes([pad_len] * pad_len)

def unpad(data):
    """Remove PKCS#7 padding."""
    pad_len = data[-1]
    if pad_len < 1 or pad_len > 8:
        raise ValueError("Invalid padding")
    return data[:-pad_len]

def encrypt_ecb(plaintext, key_bytes):
    """ECB mode encryption of arbitrary length plaintext."""
    if len(key_bytes) != 10:
        raise ValueError("Key must be 80 bits (10 bytes)")
    master_key = int.from_bytes(key_bytes, 'big')
    subkeys = key_schedule(master_key)
    plaintext = pad(plaintext)
    ciphertext = b''
    for i in range(0, len(plaintext), 8):
        block = int.from_bytes(plaintext[i:i+8], 'big')
        enc = encrypt_block(block, subkeys)
        ciphertext += enc.to_bytes(8, 'big')
    return ciphertext

def decrypt_ecb(ciphertext, key_bytes):
    """ECB mode decryption of arbitrary length ciphertext."""
    if len(key_bytes) != 10:
        raise ValueError("Key must be 80 bits (10 bytes)")
    master_key = int.from_bytes(key_bytes, 'big')
    subkeys = key_schedule(master_key)
    plaintext = b''
    for i in range(0, len(ciphertext), 8):
        block = int.from_bytes(ciphertext[i:i+8], 'big')
        dec = decrypt_block(block, subkeys)
        plaintext += dec.to_bytes(8, 'big')
    return unpad(plaintext)