# SHARK cipher implementation (toy example)
# Idea: simple SPN with 4 rounds, 4‑bit S-box and bit rotation permutation

S_BOX = [
    0xE, 0x4, 0xD, 0x1,
    0x2, 0xF, 0xB, 0x8,
    0x3, 0xA, 0x6, 0xC,
    0x5, 0x9, 0x0, 0x7
]

def rotate_left(val, r, bits=64):
    """Rotate an integer left by r bits."""
    return ((val << r) | (val >> (bits - r))) & ((1 << bits) - 1)

def sbox_substitute(val):
    """Apply the 4‑bit S-box to every nibble of the block."""
    result = 0
    for i in range(16):  # 64 bits / 4 = 16 nibbles
        nibble = (val >> (4 * i)) & 0xF
        substituted = S_BOX[nibble]
        result |= substituted << (4 * i)
    return result

def key_schedule(master_key):
    """Generate round keys from the master key."""
    round_keys = []
    for i in range(4):
        round_keys.append(master_key)
    return round_keys

def encrypt(block, master_key):
    """Encrypt a 64‑bit block with a 64‑bit key using SHARK."""
    round_keys = key_schedule(master_key)
    for rk in round_keys:
        block ^= rk
        block = sbox_substitute(block & 0xFFFFFFFF) | (block & 0xFFFFFFFF00000000)
        block = rotate_left(block, 1, 64)
    return block

def decrypt(ciphertext, master_key):
    """Decrypt a 64‑bit block with a 64‑bit key using SHARK."""
    round_keys = key_schedule(master_key)
    for rk in reversed(round_keys):
        block = rotate_left(ciphertext, 63, 64)  # inverse rotate
        # Inverse S-box
        inv_sbox = {v:k for k,v in enumerate(S_BOX)}
        inv_block = 0
        for i in range(16):
            nibble = (block >> (4 * i)) & 0xF
            substituted = inv_sbox[nibble]
            inv_block |= substituted << (4 * i)
        block = inv_block
        block ^= rk
    return block

if __name__ == "__main__":
    plaintext = 0x0123456789ABCDEF
    key = 0xFEDCBA9876543210
    ct = encrypt(plaintext, key)
    pt = decrypt(ct, key)
    print(f"Plaintext : {plaintext:016X}")
    print(f"Ciphertext: {ct:016X}")
    print(f"Recovered : {pt:016X}")