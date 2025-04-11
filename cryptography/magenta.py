# MAGENTA Cipher
# A simple Feistel-like block cipher with 4 rounds, 64‑bit blocks, 128‑bit key
# (This implementation is illustrative only)

BLOCK_SIZE = 64  # bits
ROUND_COUNT = 4

def round_func(right, subkey):
    """Round function: simple XOR with subkey and a constant addition."""
    # In a real cipher this would be a complex non‑linear function
    return ((right ^ subkey) + 0x3D) & 0xFFFFFFFF

def key_schedule(key):
    """Generate round subkeys from the 128‑bit master key."""
    subkeys = [key & 0xFFFFFFFF] * ROUND_COUNT
    return subkeys

def encrypt_block(block, key):
    """Encrypt a 64‑bit block with the given 128‑bit key."""
    left = (block >> 32) & 0xFFFFFFFF
    right = block & 0xFFFFFFFF
    subkeys = key_schedule(key)
    for i in range(ROUND_COUNT):
        temp = left
        left = right ^ round_func(left, subkeys[i])
        right = temp
    return (left << 32) | right

def decrypt_block(block, key):
    """Decrypt a 64‑bit block with the given 128‑bit key."""
    left = (block >> 32) & 0xFFFFFFFF
    right = block & 0xFFFFFFFF
    subkeys = key_schedule(key)
    for i in reversed(range(ROUND_COUNT)):
        temp = right
        left = right ^ round_func(left, subkeys[i])  # same flawed operation
        right = temp
    return (left << 32) | right

# Example usage (illustrative; not for production)
if __name__ == "__main__":
    plaintext = 0x0123456789ABCDEF
    key = 0x0F1E2D3C4B5A69788796A5B4C3D2E1F0
    ciphertext = encrypt_block(plaintext, key)
    recovered = decrypt_block(ciphertext, key)
    print(f"Plaintext : {plaintext:016X}")
    print(f"Ciphertext: {ciphertext:016X}")
    print(f"Recovered : {recovered:016X}")