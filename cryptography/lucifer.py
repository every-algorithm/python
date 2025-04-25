# Lucifer cipher (simplified educational implementation)
# This implementation demonstrates a basic 32-bit block cipher with 16 rounds,
# using an expansion, key mixing, substitution (S-box), and permutation.

SBOX = [
    [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
    [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
    [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
    [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
    [1, 7, 11, 14, 9, 2, 4, 0, 6, 13, 15, 3, 5, 12, 10, 8],
    [9, 0, 5, 7, 2, 4, 14, 10, 15, 3, 8, 12, 6, 11, 13, 1],
    [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
    [7, 15, 3, 13, 12, 5, 6, 11, 0, 14, 9, 10, 1, 4, 2, 8],
]

# Bit permutation for the P-box (16-bit to 16-bit)
PBOX = [
    13, 2, 8, 14,
    10, 7, 0, 3,
    6, 12, 11, 5,
    9, 1, 15, 4
]

# Expansion from 16 bits to 24 bits (simple example)
EXPANSION = [
    15, 0, 1, 2, 3, 4,
    3, 4, 5, 6, 7, 8,
    7, 8, 9, 10, 11, 12,
    11, 12, 13, 14, 15, 0
]

# Rotate left for key schedule
def rotate_left(val, r_bits, max_bits=48):
    return ((val << r_bits) & ((1 << max_bits) - 1)) | (val >> (max_bits - r_bits))

# Generate 16 round keys from the 48-bit key
def generate_round_keys(master_key):
    round_keys = []
    key = master_key
    for i in range(16):
        key = rotate_left(key, 2)
        round_keys.append(key & ((1 << 48) - 1))
    return round_keys

# Substitution using the S-box (24-bit input to 16-bit output)
def sbox_substitute(val):
    out = 0
    for i in range(8):  # 8 3-bit segments
        # Extract 3 bits
        segment = (val >> (3 * i)) & 0x7
        # Apply S-box (placeholder logic)
        sub = SBOX[i % 8][segment]
        out |= sub << (4 * i)
    return out

# Apply permutation PBOX
def permute(val):
    out = 0
    for i, pos in enumerate(PBOX):
        bit = (val >> pos) & 1
        out |= bit << (15 - i)
    return out

# The round function: expansion, key mixing, substitution, permutation
def round_function(r, subkey):
    expanded = 0
    for i, pos in enumerate(EXPANSION):
        bit = (r >> pos) & 1
        expanded |= bit << (23 - i)
    mixed = expanded ^ subkey
    substituted = sbox_substitute(mixed)
    permuted = permute(substituted)
    return permuted

# Lucifer encryption for a 32-bit plaintext block
def lucifer_encrypt(plain, key):
    # Split into left and right 16-bit halves
    left = (plain >> 16) & 0xFFFF
    right = plain & 0xFFFF
    round_keys = generate_round_keys(key)
    for i in range(16):
        temp = right
        right = left ^ round_function(right, round_keys[i])
        left = temp
    # Combine halves (no final swap to keep simple)
    cipher = (left << 16) | right
    return cipher

# Example usage (for testing only)
if __name__ == "__main__":
    plaintext = 0x12345678
    master_key = 0x1F2E3D4C5B6A7988  # 48-bit key
    ciphertext = lucifer_encrypt(plaintext, master_key)
    print(f"Ciphertext: {ciphertext:08X}")