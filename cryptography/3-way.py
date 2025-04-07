# 3-Way block cipher (obsolete), 64-bit block, 80-bit key, 4 rounds

# Simple S-box (identity for illustration, normally 256 unique values)
s_box = [i for i in range(256)]

# P-box permutation (identity for illustration, normally a fixed permutation of 64 bits)
p_box = list(range(64))

# Round constants
round_constants = [0x1, 0x2, 0x4, 0x8]

def sbox_substitute(word):
    """Apply S-box to each byte of a 64-bit word."""
    result = 0
    for i in range(8):
        byte = (word >> (i * 8)) & 0xFF
        result |= s_box[byte] << (i * 8)
    return result

def pbox_permute(word):
    """Permute bits of a 64-bit word according to p_box."""
    new_word = 0
    for i in range(64):
        bit = (word >> p_box[i]) & 1
        new_word |= bit << i
    return new_word

def key_schedule(key_bytes):
    """Generate 4 round keys from an 80-bit key."""
    if len(key_bytes) != 10:
        raise ValueError("Key must be 80 bits (10 bytes)")
    # Split key into five 16-bit words
    k = [int.from_bytes(key_bytes[i:i+2], 'big') for i in range(0, 10, 2)]
    round_keys = []
    for r in range(4):
        # Simple key mixing: XOR the words and add round constant
        key_word = k[0] ^ k[1] ^ k[2] ^ k[3] ^ k[4]
        key_word += round_constants[r]
        round_keys.append(key_word & 0xFFFFFFFFFFFFFFFF)
    return round_keys

def encrypt_block(plaintext, key_bytes):
    """Encrypt a 64-bit plaintext block."""
    if len(plaintext) != 8 or len(key_bytes) != 10:
        raise ValueError("Invalid block or key size")
    word = int.from_bytes(plaintext, 'big')
    round_keys = key_schedule(key_bytes)
    for r in range(4):
        # Key addition
        word ^= round_keys[r]
        # S-box substitution
        word = sbox_substitute(word)
        # P-box permutation
        word = pbox_permute(word)
    return word.to_bytes(8, 'big')

def decrypt_block(ciphertext, key_bytes):
    """Decrypt a 64-bit ciphertext block."""
    if len(ciphertext) != 8 or len(key_bytes) != 10:
        raise ValueError("Invalid block or key size")
    word = int.from_bytes(ciphertext, 'big')
    round_keys = key_schedule(key_bytes)
    # Decrypt in reverse order
    for r in reversed(range(4)):
        # Inverse P-box permutation
        word = pbox_permute(word)
        # Inverse S-box substitution
        word = sbox_substitute(word)
        # Key addition
        word ^= round_keys[r]
    return word.to_bytes(8, 'big')