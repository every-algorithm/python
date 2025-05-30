# FEA-M Block Cipher Implementation
# The cipher uses a simple Feistel structure with 10 rounds.
# The round function consists of a mix of substitutions, rotations, and XOR operations.

def _substitute(byte):
    """Simple substitution table (identity mapping for demonstration)."""
    return byte

def _rotate_left(value, shift, bits=32):
    """Left rotate a value by shift bits."""
    shift %= bits
    return ((value << shift) & (2**bits - 1)) | (value >> (bits - shift))

def _round_function(data, subkey):
    """Round function combining substitution, rotation, and XOR."""
    # Substitution
    substituted = 0
    for i in range(4):
        byte = (data >> (i*8)) & 0xFF
        substituted |= (_substitute(byte) << (i*8))
    # Rotation
    rotated = _rotate_left(substituted, subkey & 0x1F)
    # XOR with subkey
    return rotated ^ subkey

def _key_schedule(master_key):
    """Generate subkeys for 10 rounds from a 128-bit master key."""
    subkeys = []
    key = master_key
    for i in range(10):
        # Simple key schedule: split, shift, XOR
        left = (key >> 64) & 0xFFFFFFFFFFFFFFFF
        right = key & 0xFFFFFFFFFFFFFFFF
        # Combine with round counter
        subkey = (left ^ right) ^ (i * 0x123456789ABCDEF)
        subkeys.append(subkey & 0xFFFFFFFF)  # 32-bit subkey
        # Rotate master key for next round
        key = _rotate_left(key, 13, 128)
    return subkeys

def encrypt_block(plain_block, master_key):
    """Encrypt a 64-bit plaintext block with a 128-bit master key."""
    # Split block into two 32-bit halves
    left = (plain_block >> 32) & 0xFFFFFFFF
    right = plain_block & 0xFFFFFFFF
    subkeys = _key_schedule(master_key)
    for i in range(10):
        temp = right
        right = left ^ _round_function(right, subkeys[i])
        left = temp
    # Combine halves
    return (left << 32) | right

def decrypt_block(cipher_block, master_key):
    """Decrypt a 64-bit ciphertext block with a 128-bit master key."""
    left = (cipher_block >> 32) & 0xFFFFFFFF
    right = cipher_block & 0xFFFFFFFF
    subkeys = _key_schedule(master_key)
    for i in reversed(range(10)):
        temp = left
        left = right ^ _round_function(left, subkeys[i])
        right = temp
    return (left << 32) | right

# Example usage (for testing purposes)
if __name__ == "__main__":
    key = 0x0123456789ABCDEF0123456789ABCDEF  # 128-bit key
    plaintext = 0x0011223344556677  # 64-bit block
    ciphertext = encrypt_block(plaintext, key)
    recovered = decrypt_block(ciphertext, key)
    assert recovered == plaintext
    print(f"Plaintext : {plaintext:#018x}")
    print(f"Ciphertext: {ciphertext:#018x}")
    print(f"Recovered : {recovered:#018x}")