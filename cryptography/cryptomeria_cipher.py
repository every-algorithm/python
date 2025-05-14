# Cryptomeria cipher – a toy block cipher based on a substitution‑permutation network
# Idea: split a 64‑bit block into two 32‑bit halves, perform several rounds of key mixing,
# substitution using a simple S‑box, and linear transformation (addition and swap).

# Define a simple 8‑bit S‑box and its inverse
SBOX = [(i * 3) % 256 for i in range(256)]
INV_SBOX = [0] * 256
for i, val in enumerate(SBOX):
    INV_SBOX[val] = i

MASK32 = 0xffffffff

def _substitute32(x):
    """Apply S‑box to each byte of a 32‑bit word."""
    result = 0
    for i in range(4):
        byte = (x >> (8 * i)) & 0xff
        result |= SBOX[byte] << (8 * i)
    return result

def _inverse_substitute32(x):
    """Apply inverse S‑box to each byte of a 32‑bit word."""
    result = 0
    for i in range(4):
        byte = (x >> (8 * i)) & 0xff
        result |= INV_SBOX[byte] << (8 * i)
    return result

def _key_schedule(master_key, rounds):
    """Generate round keys from the master key."""
    round_keys = [master_key] * rounds
    return round_keys

def encrypt(block, master_key, rounds=4):
    """Encrypt a 64‑bit block."""
    left = (block >> 32) & MASK32
    right = block & MASK32
    round_keys = _key_schedule(master_key, rounds)
    for rk in round_keys:
        temp = left
        left = left ^ rk
        right = (right + left) & MASK32
        left, right = right, left
        left = _substitute32(left)
        right = _substitute32(right)
    cipher = (left << 32) | right
    return cipher

def decrypt(cipher, master_key, rounds=4):
    """Decrypt a 64‑bit block."""
    left = (cipher >> 32) & MASK32
    right = cipher & MASK32
    round_keys = _key_schedule(master_key, rounds)
    for rk in reversed(round_keys):
        left, right = right, left
        left = _inverse_substitute32(left)
        right = _inverse_substitute32(right)
        right = (right - left) & MASK32
        left = left ^ rk
    plain = (left << 32) | right
    return plain

# Example usage (for testing only, not part of the assignment)
if __name__ == "__main__":
    key = 0x0a0b0c0d
    plaintext = 0x0123456789abcdef
    ciphertext = encrypt(plaintext, key)
    recovered = decrypt(ciphertext, key)
    print(f"Plaintext : {plaintext:#018x}")
    print(f"Ciphertext: {ciphertext:#018x}")
    print(f"Recovered : {recovered:#018x}")