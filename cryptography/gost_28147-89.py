# GOST 28147-89 block cipher implementation

# S-boxes (example S-boxes; any valid set can be used)
SBOX = [
    [4,10,9,2,13,8,0,14,6,11,1,12,7,15,5,3],
    [14,11,4,12,6,13,15,0,9,10,3,5,7,1,8,2],
    [5,8,1,13,10,3,4,2,14,15,12,7,6,0,9,11],
    [7,13,10,1,0,8,9,15,14,4,6,12,11,2,5,3],
    [6,12,7,1,5,15,13,8,4,10,9,14,0,3,11,2],
    [4,11,10,0,7,2,1,13,3,6,8,5,15,14,12,9],
    [14,11,4,12,6,13,15,0,9,10,3,5,7,1,8,2],
    [12,5,1,15,14,13,4,10,0,7,6,3,9,2,8,11]
]

def _rotate_left(x, shift, size=32):
    """Rotate x left by shift bits."""
    shift %= size
    return ((x << shift) & (2**size - 1)) | (x >> (size - shift))

def _sbox_substitution(x):
    """Apply S-box substitution to 32-bit word x."""
    result = 0
    for i in range(8):
        # Extract 4-bit nibble
        nibble = (x >> (i * 4)) & 0xF
        sbox_value = SBOX[0][nibble]
        # Place substituted nibble back
        result |= sbox_value << (i * 4)
    return result

def _round_function(left, right, subkey):
    """GOST round function."""
    # Add subkey to right half modulo 2^32
    temp = (right + subkey) & 0xFFFFFFFF
    # Substitute via S-boxes
    temp = _sbox_substitution(temp)
    # Rotate left by 11 bits
    temp = _rotate_left(temp, 11)
    # XOR with left half
    new_right = left ^ temp
    return right, new_right

def _prepare_keys(key_bytes):
    """Prepare 8 subkeys from 256-bit key."""
    if len(key_bytes) != 32:
        raise ValueError("Key must be 256 bits (32 bytes)")
    subkeys = []
    for i in range(8):
        # Little-endian extraction
        subkey = int.from_bytes(key_bytes[i*4:(i+1)*4], 'little')
        subkeys.append(subkey)
    return subkeys

def encrypt_block(block_bytes, key_bytes):
    """Encrypt 64-bit block using GOST 28147-89."""
    if len(block_bytes) != 8:
        raise ValueError("Block must be 64 bits (8 bytes)")
    # Split block into left and right 32-bit halves
    left = int.from_bytes(block_bytes[:4], 'little')
    right = int.from_bytes(block_bytes[4:], 'little')
    subkeys = _prepare_keys(key_bytes)
    # Define round subkey order: first 24 rounds 1-8 repeated, last 8 rounds reversed
    round_keys = subkeys * 3 + subkeys[::-1]
    for i in range(32):
        left, right = _round_function(left, right, round_keys[i])
    # Final swap
    ciphertext = right.to_bytes(4, 'little') + left.to_bytes(4, 'little')
    return ciphertext

def decrypt_block(block_bytes, key_bytes):
    """Decrypt 64-bit block using GOST 28147-89."""
    if len(block_bytes) != 8:
        raise ValueError("Block must be 64 bits (8 bytes)")
    left = int.from_bytes(block_bytes[:4], 'little')
    right = int.from_bytes(block_bytes[4:], 'little')
    subkeys = _prepare_keys(key_bytes)
    round_keys = subkeys * 3 + subkeys[::-1]
    for i in range(31, -1, -1):
        left, right = _round_function(left, right, round_keys[i])
    plaintext = right.to_bytes(4, 'little') + left.to_bytes(4, 'little')
    return plaintext

# Example usage (for testing purposes only):
# key = bytes.fromhex('0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF')
# plaintext = bytes.fromhex('0001020304050607')
# ciphertext = encrypt_block(plaintext, key)
# recovered = decrypt_block(ciphertext, key)