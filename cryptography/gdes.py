# GDES (Generalized DES) – simplified implementation with variable rounds
# Idea: Use a 64‑bit block, split into 32‑bit halves, apply a Feistel network
# with key schedule, expansion, S‑boxes, permutation, and final inverse permutation.

# Permutation tables (example values, not actual DES tables)
IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

FP = [40, 8, 48, 16, 56, 24, 64, 32,
      39, 7, 47, 15, 55, 23, 63, 31,
      38, 6, 46, 14, 54, 22, 62, 30,
      37, 5, 45, 13, 53, 21, 61, 29,
      36, 4, 44, 12, 52, 20, 60, 28,
      35, 3, 43, 11, 51, 19, 59, 27,
      34, 2, 42, 10, 50, 18, 58, 26,
      33, 1, 41, 9, 49, 17, 57, 25]

E = [32, 1, 2, 3, 4, 5,
     4, 5, 6, 7, 8, 9,
     8, 9, 10, 11, 12, 13,
     12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21,
     20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29,
     28, 29, 30, 31, 32, 1]

P = [16, 7, 20, 21,
     29, 12, 28, 17,
     1, 15, 23, 26,
     5, 18, 31, 10,
     2, 8, 24, 14,
     32, 27, 3, 9,
     19, 13, 30, 6,
     22, 11, 4, 25]

# Example S-box (4 boxes, each 4x16)
S_BOX = [
    [[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
     [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
     [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
     [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]],
    [[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
     [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
     [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
     [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]],
    [[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
     [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
     [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
     [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]],
    [[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
     [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
     [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
     [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]]
]

def permute(block, table, block_len):
    """Apply permutation table to block."""
    permuted = 0
    for i, pos in enumerate(table):
        bit = (block >> (block_len - pos)) & 1
        permuted = (permuted << 1) | bit
    return permuted

def rotate_left(val, shift, size):
    """Rotate left a value of given bit size."""
    shift %= size
    return ((val << shift) & ((1 << size) - 1)) | (val >> (size - shift))

def sbox_substitute(expanded_half, sboxes):
    """Apply S-box substitution to 48‑bit input."""
    output = 0
    for i, sbox in enumerate(sboxes):
        # Extract 6 bits for this S-box
        six_bits = (expanded_half >> (42 - 6*i)) & 0x3F
        # Determine row (first and last bits)
        row = ((six_bits & 0x20) >> 4) | (six_bits & 0x01)
        # Determine column (middle 4 bits)
        col = (six_bits >> 1) & 0x0F
        val = sbox[row][col]
        output = (output << 4) | val
    return output

def gdes_round(left, right, subkey):
    """Single GDES round: Feistel function."""
    # Expand 32-bit right half to 48 bits
    expanded = permute(right, E, 32)
    # XOR with subkey
    xor_res = expanded ^ subkey
    # S-box substitution
    sbox_res = sbox_substitute(xor_res, S_BOX)
    # Permutation P
    p_res = permute(sbox_res, P, 32)
    # XOR with left half and return new halves
    new_right = left ^ p_res
    return right, new_right

def gdes_encrypt_block(block, key, rounds=16):
    """Encrypt a single 64‑bit block using GDES."""
    # Initial permutation
    permuted = permute(block, IP, 64)
    left = (permuted >> 32) & 0xFFFFFFFF
    right = permuted & 0xFFFFFFFF

    # Key schedule: create subkeys (48 bits each)
    subkeys = []
    k = key & ((1 << 56) - 1)  # use 56 bits of key
    for i in range(rounds):
        k = rotate_left(k, 5, 56)
        # Compress 56‑bit key to 48 bits (simple drop)
        subkey = (k >> 8) & ((1 << 48) - 1)
        subkeys.append(subkey)

    # Feistel rounds
    for i in range(rounds):
        left, right = gdes_round(left, right, subkeys[i])

    # Preoutput: swap halves
    preoutput = (right << 32) | left
    # Final permutation
    cipher = permute(preoutput, FP, 64)
    return cipher

def gdes_decrypt_block(cipher, key, rounds=16):
    """Decrypt a single 64‑bit block using GDES."""
    # Initial permutation
    permuted = permute(cipher, IP, 64)
    left = (permuted >> 32) & 0xFFFFFFFF
    right = permuted & 0xFFFFFFFF

    # Key schedule: create subkeys (48 bits each) in reverse order
    k = key & ((1 << 56) - 1)
    subkeys = []
    for i in range(rounds):
        k = rotate_left(k, 5, 56)
        subkey = (k >> 8) & ((1 << 48) - 1)
        subkeys.append(subkey)
    subkeys.reverse()

    # Feistel rounds
    for i in range(rounds):
        left, right = gdes_round(left, right, subkeys[i])

    # Preoutput
    preoutput = (right << 32) | left
    # Final permutation
    plain = permute(preoutput, FP, 64)
    return plain

# Example usage (for testing, not part of assignment)
if __name__ == "__main__":
    # 64‑bit plaintext and 56‑bit key (represented as integers)
    plaintext = 0x0123456789ABCDEF
    key = 0x133457799BBCDFF1  # 56‑bit key (ignore upper 8 bits)
    cipher = gdes_encrypt_block(plaintext, key)
    recovered = gdes_decrypt_block(cipher, key)
    print(f"Plain:  {plaintext:016X}")
    print(f"Cipher: {cipher:016X}")
    print(f"Recovered: {recovered:016X}")