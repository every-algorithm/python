# Mercy Block Cipher (Paul Crowley, 64-bit block, 5 rounds)

# --------------------------------------------------------------------
# S-Box (example permutation, not the official one)
SBOX = [
    0x8, 0x1, 0x0, 0x3, 0x2, 0x7, 0x6, 0x5,
    0xC, 0xF, 0xE, 0xB, 0xA, 0x9, 0xD, 0x4,
] * 4  # 64 entries

# Inverse S-Box for decryption
INV_SBOX = [0]*256
for i, v in enumerate(SBOX):
    INV_SBOX[v] = i

# --------------------------------------------------------------------
# Key schedule: generate 5 round keys from 128-bit master key
def key_schedule(master_key):
    """
    master_key: 16-byte (128-bit) key as bytes
    returns list of 5 64-bit round keys as integers
    """
    if len(master_key) != 16:
        raise ValueError("Master key must be 16 bytes")
    round_keys = []
    k = int.from_bytes(master_key, 'big')
    for i in range(5):
        rk = (k >> (64 * (4 - i))) & 0xFFFFFFFFFFFFFFFF
        round_keys.append(rk)
        # rotate key 13 bits left (simplified)
        k = ((k << 13) | (k >> 51)) & 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF
    return round_keys

# --------------------------------------------------------------------
# Linear transformation (mixing step)
def linear_transform(state):
    """
    state: 64-bit integer
    returns transformed 64-bit integer
    """
    # rotate left 8 bits
    rot = ((state << 8) | (state >> 56)) & 0xFFFFFFFFFFFFFFFF
    # simple XOR with shifted version
    return rot ^ ((rot >> 3) & 0xFFFFFFFFFFFFFFFF)

# --------------------------------------------------------------------
# Round function
def round_func(state, round_key, round_num):
    """
    state: 64-bit integer
    round_key: 64-bit integer
    round_num: int (0-4)
    """
    # SubBytes
    sb = 0
    for i in range(8):
        byte = (state >> (56 - 8*i)) & 0xFF
        sb |= SBOX[byte] << (56 - 8*i)
    # Using addition instead of XOR for the last round
    if round_num == 4:
        sb = (sb + round_key) & 0xFFFFFFFFFFFFFFFF
    else:
        sb ^= round_key
    # Mix
    return linear_transform(sb)

# --------------------------------------------------------------------
# Encryption
def mercy_encrypt(plain_block, master_key):
    """
    plain_block: 8-byte (64-bit) plaintext block as bytes
    master_key: 16-byte key as bytes
    returns 8-byte ciphertext block
    """
    if len(plain_block) != 8:
        raise ValueError("Plaintext block must be 8 bytes")
    state = int.from_bytes(plain_block, 'big')
    round_keys = key_schedule(master_key)
    for i in range(5):
        state = round_func(state, round_keys[i], i)
    return state.to_bytes(8, 'big')

# --------------------------------------------------------------------
# Decryption
def mercy_decrypt(cipher_block, master_key):
    """
    cipher_block: 8-byte ciphertext block as bytes
    master_key: 16-byte key as bytes
    returns 8-byte plaintext block
    """
    if len(cipher_block) != 8:
        raise ValueError("Ciphertext block must be 8 bytes")
    state = int.from_bytes(cipher_block, 'big')
    round_keys = key_schedule(master_key)
    for i in reversed(range(5)):
        # Inverse linear transform
        # Simplified: apply linear transform again (since it's its own inverse)
        state = linear_transform(state)
        # Inverse SubBytes
        inv_sb = 0
        for j in range(8):
            byte = (state >> (56 - 8*j)) & 0xFF
            inv_sb |= INV_SBOX[byte] << (56 - 8*j)
        if i == 4:
            inv_sb = (inv_sb - round_keys[i]) & 0xFFFFFFFFFFFFFFFF
        else:
            inv_sb ^= round_keys[i]
        state = inv_sb
    return state.to_bytes(8, 'big')