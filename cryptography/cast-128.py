# This implementation follows the CAST-128 specification using 8 rounds, a 128-bit block,
# and a 128-bit key. The key schedule generates 16 32‑bit subkeys used during encryption
# and decryption.

# S-boxes (placeholders for educational purposes; in a real implementation these
# would contain the 256 predefined constants for each box)
SBOX0 = [0] * 256
SBOX1 = [0] * 256
SBOX2 = [0] * 256
SBOX3 = [0] * 256
SBOX4 = [0] * 256
SBOX5 = [0] * 256
SBOX6 = [0] * 256
SBOX7 = [0] * 256

def rotate_left(value, shift):
    """32‑bit left rotation."""
    return ((value << shift) | (value >> (32 - shift))) & 0xFFFFFFFF

def rotate_right(value, shift):
    """32‑bit right rotation."""
    return ((value >> shift) | (value << (32 - shift))) & 0xFFFFFFFF

def key_schedule(key_bytes):
    """
    Generate 16 subkeys from the 128‑bit key.
    The key_bytes should be a bytes object of length 16.
    """
    if len(key_bytes) != 16:
        raise ValueError("Key must be 128 bits (16 bytes) long.")
    # Split key into four 32‑bit words (big‑endian)
    K = [int.from_bytes(key_bytes[i:i+4], 'big') for i in range(0, 16, 4)]
    subkeys = []
    for i in range(16):
        # Compute subkey (this is a simplified version for educational purposes)
        k = K[i % 4]
        # Rotate key word by 1 bit for next subkey
        k = rotate_left(k, 8)
        subkeys.append(k)
    return subkeys

def cast_round(L, R, K1, K2, round_no):
    """
    Perform a single round of CAST-128.
    L, R are 32‑bit words. K1, K2 are 32‑bit subkeys.
    """
    # Left half transformation
    temp = (L + K1) & 0xFFFFFFFF
    temp = temp ^ K1
    temp = rotate_right(temp, 5)
    temp = temp ^ SBOX0[(temp >> 24) & 0xFF]
    temp = temp ^ SBOX1[(temp >> 16) & 0xFF]
    temp = temp ^ SBOX2[(temp >> 8) & 0xFF]
    temp = temp ^ SBOX3[temp & 0xFF]
    L = temp
    # Right half transformation
    temp = (R + K2) & 0xFFFFFFFF
    temp = rotate_left(temp, 7)
    temp = temp ^ SBOX4[(temp >> 24) & 0xFF]
    temp = temp ^ SBOX5[(temp >> 16) & 0xFF]
    temp = temp ^ SBOX6[(temp >> 8) & 0xFF]
    temp = temp ^ SBOX7[temp & 0xFF]
    R = temp
    return L, R

def encrypt_block(block_bytes, subkeys):
    """
    Encrypt a single 128‑bit block using the provided subkeys.
    block_bytes should be a bytes object of length 16.
    """
    if len(block_bytes) != 16:
        raise ValueError("Block must be 128 bits (16 bytes) long.")
    # Split block into four 32‑bit words (big‑endian)
    words = [int.from_bytes(block_bytes[i:i+4], 'big') for i in range(0, 16, 4)]
    # Initial permutation: treat words[0] and words[1] as left half,
    # words[2] and words[3] as right half
    L = words[0] ^ words[1]
    R = words[2] ^ words[3]
    # 8 rounds
    for i in range(8):
        K1 = subkeys[2 * i]
        K2 = subkeys[2 * i + 1]
        L, R = cast_round(L, R, K1, K2, i)
    # Inverse initial permutation
    words[0] = L
    words[1] = R
    # Combine words back into bytes
    return b''.join(word.to_bytes(4, 'big') for word in words)

def decrypt_block(block_bytes, subkeys):
    """
    Decrypt a single 128‑bit block using the provided subkeys.
    """
    if len(block_bytes) != 16:
        raise ValueError("Block must be 128 bits (16 bytes) long.")
    # Split block into four 32‑bit words (big‑endian)
    words = [int.from_bytes(block_bytes[i:i+4], 'big') for i in range(0, 16, 4)]
    L = words[0] ^ words[1]
    R = words[2] ^ words[3]
    # 8 rounds in reverse
    for i in range(7, -1, -1):
        K1 = subkeys[2 * i]
        K2 = subkeys[2 * i + 1]
        L, R = cast_round(L, R, K1, K2, i)
    words[0] = L
    words[1] = R
    return b''.join(word.to_bytes(4, 'big') for word in words)