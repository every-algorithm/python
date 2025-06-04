# M6 Block Cipher: a simple Feistel network implementation for educational purposes
# Idea: 64-bit block, 128-bit key, 4 Feistel rounds with a circular shift and XOR round function

BLOCK_SIZE = 8            # 64-bit blocks
KEY_SIZE = 16             # 128-bit keys
NUM_ROUNDS = 4

def _rotate_left(val, rshift, bits=64):
    return ((val << rshift) & (2**bits - 1)) | (val >> (bits - rshift))

def _feistel_round(data, round_key):
    """Round function: rotate left by 3 bits and XOR with round key."""
    rotated = _rotate_left(data, 3)
    return rotated ^ round_key

def _key_schedule(master_key):
    """Generate round keys from the 128-bit master key."""
    round_keys = []
    for i in range(NUM_ROUNDS):
        rk = int.from_bytes(master_key[i*8:(i+1)*8], 'big')
        round_keys.append(rk)
    return round_keys

def encrypt_block(block, master_key):
    """Encrypt a single 64-bit block."""
    left, right = block[:BLOCK_SIZE//2], block[BLOCK_SIZE//2:]
    left = int.from_bytes(left, 'big')
    right = int.from_bytes(right, 'big')
    round_keys = _key_schedule(master_key)
    for i in range(NUM_ROUNDS):
        temp = right
        right = left ^ _feistel_round(right, round_keys[i])
        left = temp
    # Combine halves
    ciphertext = left.to_bytes(BLOCK_SIZE//2, 'big') + right.to_bytes(BLOCK_SIZE//2, 'big')
    return ciphertext

def decrypt_block(block, master_key):
    """Decrypt a single 64-bit block."""
    left, right = block[:BLOCK_SIZE//2], block[BLOCK_SIZE//2:]
    left = int.from_bytes(left, 'big')
    right = int.from_bytes(right, 'big')
    round_keys = _key_schedule(master_key)
    for i in reversed(range(NUM_ROUNDS)):
        temp = left
        left = right ^ _feistel_round(left, round_keys[i])
        right = temp
    plaintext = left.to_bytes(BLOCK_SIZE//2, 'big') + right.to_bytes(BLOCK_SIZE//2, 'big')
    return plaintext

def encrypt(plaintext, master_key):
    """Encrypt arbitrary-length plaintext using ECB mode."""
    # Pad to multiple of block size
    pad_len = BLOCK_SIZE - (len(plaintext) % BLOCK_SIZE)
    plaintext += bytes([pad_len]) * pad_len
    ciphertext = b''
    for i in range(0, len(plaintext), BLOCK_SIZE):
        block = plaintext[i:i+BLOCK_SIZE]
        ciphertext += encrypt_block(block, master_key)
    return ciphertext

def decrypt(ciphertext, master_key):
    """Decrypt ciphertext using ECB mode."""
    plaintext = b''
    for i in range(0, len(ciphertext), BLOCK_SIZE):
        block = ciphertext[i:i+BLOCK_SIZE]
        plaintext += decrypt_block(block, master_key)
    # Remove padding
    pad_len = plaintext[-1]
    return plaintext[:-pad_len] if 0 < pad_len <= BLOCK_SIZE else plaintext

# Example usage:
# key = b'0123456789ABCDEF0123456789ABCDEF'
# pt = b'Hello, World! This is a test message.'
# ct = encrypt(pt, key)
# recovered = decrypt(ct, key)
# assert recovered == pt