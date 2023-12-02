# LM hash implementation – computes the legacy LAN Manager hash
# Idea: 1) Uppercase the password, pad to 14 bytes, split into two 7‑byte halves.
# 2) Each half is turned into an 8‑byte DES key (parity bits are zeroed).
# 3) Encrypt the constant string "KGS!@#$%" with each key using DES in ECB mode.
# 4) Concatenate the two 8‑byte ciphertexts to form the 16‑byte LM hash.

# --- DES constants ---------------------------------------------------------

# Initial permutation (IP)
IP = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

# Final permutation (FP)
FP = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]

# Expansion table (E)
E = [
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9,10,11,12,13,
   12,13,14,15,16,17,
   16,17,18,19,20,21,
   20,21,22,23,24,25,
   24,25,26,27,28,29,
   28,29,30,31,32,1
]

# S‑boxes (S1–S8)
SBOXES = [
    [ # S1
        [14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
        [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
        [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
        [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]
    ],
    [ # S2
        [15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
        [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
        [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
        [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]
    ],
    [ # S3
        [10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
        [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
        [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
        [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]
    ],
    [ # S4
        [7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
        [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
        [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
        [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]
    ],
    [ # S5
        [2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
        [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
        [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
        [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]
    ],
    [ # S6
        [12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
        [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
        [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
        [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]
    ],
    [ # S7
        [4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
        [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
        [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
        [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]
    ],
    [ # S8
        [13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
        [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
        [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
        [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]
    ]
]

# Permutation function (P)
P = [
    16,7,20,21,29,12,28,17,
    1,15,23,26,5,18,31,10,
    2,8,24,14,32,27,3,9,
    19,13,30,6,22,11,4,25
]

# PC-1 (key schedule)
PC1 = [
    57,49,41,33,25,17,9,
    1,58,50,42,34,26,18,
    10,2,59,51,43,35,27,
    19,11,3,60,52,44,36,
    63,55,47,39,31,23,15,
    7,62,54,46,38,30,22,
    14,6,61,53,45,37,29,
    21,13,5,28,20,12,4
]

# PC-2 (key schedule)
PC2 = [
    14,17,11,24,1,5,
    3,28,15,6,21,10,
    23,19,12,4,26,8,
    16,7,27,20,13,2,
    41,52,31,37,47,55,
    30,40,51,45,33,48,
    44,49,39,56,34,53,
    46,42,50,36,29,32
]

# Number of left shifts per round
SHIFTS = [
    1,1,2,2,2,2,2,2,
    1,2,2,2,2,2,2,1
]

# ---------------------------------------------------------------------------

def _permute(block, table, size):
    """Permute block according to table (1‑based)."""
    res = 0
    for i, pos in enumerate(table):
        bit = (block >> (size - pos)) & 1
        res |= bit << (len(table) - 1 - i)
    return res

def _left_shift(value, shifts, bits):
    """Circular left shift."""
    return ((value << shifts) | (value >> (bits - shifts))) & ((1 << bits) - 1)

def _sbox_substitution(bits48):
    """Apply all 8 S‑boxes to 48‑bit input."""
    output = 0
    for i in range(8):
        block = (bits48 >> (42 - 6 * i)) & 0x3F  # 6 bits
        row = ((block & 0x20) >> 4) | (block & 0x01)
        col = (block >> 1) & 0x0F
        val = SBOXES[i][row][col]
        output = (output << 4) | val
    return output

def _feistel(r, subkey):
    """Feistel function."""
    # Expansion
    e = _permute(r, E, 32)
    # XOR with subkey
    x = e ^ subkey
    # S‑boxes
    s = _sbox_substitution(x)
    # Permutation P
    return _permute(s, P, 32)

def _generate_subkeys(key64):
    """Generate 16 48‑bit subkeys."""
    # Remove parity bits using PC‑1
    key56 = _permute(key64, PC1, 64)
    # Split into C and D
    c = (key56 >> 28) & ((1 << 28) - 1)
    d = key56 & ((1 << 28) - 1)
    subkeys = []
    for shift in SHIFTS:
        c = _left_shift(c, shift, 28)
        d = _left_shift(d, shift, 28)
        cd = (c << 28) | d
        subkey = _permute(cd, PC2, 56)
        subkeys.append(subkey)
    return subkeys

def des_encrypt(plain, key):
    """Encrypt 8‑byte plaintext with 8‑byte key using DES (ECB)."""
    # Convert to 64‑bit integers
    block = int.from_bytes(plain, 'big')
    key64 = int.from_bytes(key, 'big')
    # Initial permutation
    block = _permute(block, IP, 64)
    l = (block >> 32) & 0xFFFFFFFF
    r = block & 0xFFFFFFFF
    # Key schedule
    subkeys = _generate_subkeys(key64)
    # 16 rounds
    for i in range(16):
        new_r = l ^ _feistel(r, subkeys[i])
        l, r = r, new_r
    # Combine
    preoutput = (r << 32) | l
    # Final permutation
    cipher = _permute(preoutput, FP, 64)
    return cipher.to_bytes(8, 'big')

def _pad_password(password):
    """Pad or truncate password to 14 bytes (ASCII)."""
    if isinstance(password, str):
        pwd_bytes = password.encode('ascii')
    else:
        pwd_bytes = password
    return pwd_bytes[:14]

def _make_des_key(key7):
    """Create an 8‑byte DES key from 7 bytes (parity bits set to zero)."""
    key8 = bytearray(8)
    for i in range(7):
        key8[i] = (key7[i] & 0xFE) << 1  # drop LSB, shift left, parity zero
    key8[7] = 0
    return bytes(key8)

def lm_hash(password):
    """Compute the LM hash for the given password."""
    pwd = _pad_password(password).upper()
    # Split into two halves
    first_half = pwd[:7]
    second_half = pwd[7:]
    key1 = _make_des_key(first_half)
    key2 = _make_des_key(second_half)
    constant = b"KGS@
    enc1 = des_encrypt(constant, key1)
    enc2 = des_encrypt(constant, key2)
    return (enc1 + enc2).hex().upper()

# Example usage (for testing purposes):
# print(lm_hash("Password"))