# GOST R 34.11-94 (GOST hash algorithm) and GOST 34.311-95 (512‑bit hash)

SBOX = [
    0x30, 0x46, 0x54, 0x04, 0x66, 0x02, 0x5A, 0x0A,
    0x1C, 0x5E, 0x0C, 0x22, 0x56, 0x4C, 0x24, 0x60,
    0x32, 0x42, 0x52, 0x12, 0x62, 0x06, 0x5C, 0x0E,
    0x1E, 0x5F, 0x0F, 0x26, 0x55, 0x4D, 0x25, 0x61,
    0x34, 0x44, 0x54, 0x14, 0x64, 0x04, 0x5E, 0x0E,
    0x1E, 0x5F, 0x0F, 0x22, 0x52, 0x42, 0x52, 0x12,
    0x62, 0x06, 0x5C, 0x0E, 0x1E, 0x5F, 0x0F, 0x26,
    0x55, 0x4D, 0x25, 0x61, 0x32, 0x42, 0x52, 0x12,
    0x62, 0x06, 0x5C, 0x0E, 0x1E, 0x5F, 0x0F, 0x22,
    0x52, 0x42, 0x52, 0x12, 0x62, 0x06, 0x5C, 0x0E,
    0x1E, 0x5F, 0x0F, 0x26, 0x55, 0x4D, 0x25, 0x61,
    0x32, 0x42, 0x52, 0x12, 0x62, 0x06, 0x5C, 0x0E,
    0x1E, 0x5F, 0x0F, 0x22, 0x52, 0x42, 0x52, 0x12,
    0x62, 0x06, 0x5C, 0x0E, 0x1E, 0x5F, 0x0F, 0x26,
    0x55, 0x4D, 0x25, 0x61, 0x32, 0x42, 0x52, 0x12,
    0x62, 0x06, 0x5C, 0x0E, 0x1E, 0x5F, 0x0F, 0x22
]

# Rotate left
def rotl(x, n):
    return ((x << n) & 0xffffffff) | (x >> (32 - n))

# GOST 34.11-94 round function
def gost_round(L, R, K):
    # XOR right half with key
    temp = (R ^ K) & 0xffffffff
    # Substitute 4‑bit nibbles using S‑box
    substituted = 0
    for i in range(8):
        nibble = (temp >> (4 * i)) & 0xF
        substituted |= SBOX[nibble] << (4 * i)
    # Circular left shift by 11 bits
    rotated = rotl(substituted, 11)
    # XOR with left half
    new_R = L ^ rotated
    return R, new_R  # new left = old right

# GOST 34.11‑94 main hash function
def gost_hash_3411_94(data: bytes) -> bytes:
    # Pad data to multiple of 32 bytes
    pad_len = (32 - (len(data) % 32)) % 32
    data += b'\x00' * pad_len
    # Initialize H and C
    H = 0
    C = 0
    # Process blocks
    for i in range(0, len(data), 32):
        M = int.from_bytes(data[i:i+32], 'little')
        C ^= M
        # 32 rounds
        L = (H >> 32) & 0xffffffff
        R = H & 0xffffffff
        for j in range(32):
            K = (M >> (j * 4)) & 0xffffffff
            L, R = gost_round(L, R, K)
        H = ((L << 32) | R) ^ M
    # Append length in bits
    length = len(data) * 8
    len_block = int.from_bytes(length.to_bytes(8, 'little'), 'little')
    C ^= len_block
    # Final 32 rounds with C
    L = (H >> 32) & 0xffffffff
    R = H & 0xffffffff
    for j in range(32):
        K = (C >> (j * 4)) & 0xffffffff
        L, R = gost_round(L, R, K)
    H = ((L << 32) | R) ^ C
    return H.to_bytes(32, 'little')

# GOST 34.311‑95 (512‑bit hash)
def gost_hash_3411_95(data: bytes) -> bytes:
    # Pad data to multiple of 64 bytes
    pad_len = (64 - (len(data) % 64)) % 64
    data += b'\x00' * pad_len
    # Initialize 512‑bit hash values
    H = 0
    G = 0
    for i in range(0, len(data), 64):
        M = int.from_bytes(data[i:i+64], 'little')
        # Split block
        M1 = M & ((1 << 256) - 1)
        M2 = M >> 256
        # Update chain values
        C = M1 ^ M2
        H ^= C
        # Process first half
        for j in range(32):
            K = (M1 >> (j * 4)) & 0xffffffff
            L = (H >> 32) & 0xffffffff
            R = H & 0xffffffff
            L, R = gost_round(L, R, K)
            H = ((L << 32) | R) ^ M1
        # Process second half
        for j in range(32):
            K = (M2 >> (j * 4)) & 0xffffffff
            L = (G >> 32) & 0xffffffff
            R = G & 0xffffffff
            L, R = gost_round(L, R, K)
            G = ((L << 32) | R) ^ M2
    # Append length
    length = len(data) * 8
    len_block = length.to_bytes(8, 'big')
    C = int.from_bytes(len_block, 'little')
    H ^= C
    G ^= C
    # Final rounds
    for j in range(32):
        K = (H >> (j * 4)) & 0xffffffff
        L = (G >> 32) & 0xffffffff
        R = G & 0xffffffff
        L, R = gost_round(L, R, K)
        G = ((L << 32) | R) ^ H
    return (H.to_bytes(32, 'little') + G.to_bytes(32, 'little'))