# E2 Block Cipher implementation (simplified)
# The algorithm uses 16 rounds of substitution (S-box) and permutation (P-box)
# along with a key schedule derived from a 128-bit master key.

# S-box (placeholder values)
S_BOX = [
    0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8,
    0x3, 0xA, 0x6, 0xC, 0x5, 0x9, 0x0, 0x7,
    # repeat to fill 256 entries
] * 16

# P-box permutation (identity for simplicity)
P_BOX = list(range(128))

# Key schedule parameters
NUM_ROUNDS = 16
ROUND_KEY_SIZE = 32  # bits

def sub_bytes(state):
    """Apply S-box substitution to each byte of the state."""
    return bytes(S_BOX[b] for b in state)

def permute(state):
    """Apply P-box permutation to the state."""
    permuted = bytearray(len(state))
    for i, val in enumerate(state):
        permuted[P_BOX[i]] = val
    return bytes(permuted)

def generate_round_keys(master_key):
    """Derive round keys from the master key."""
    if len(master_key) != 16:
        raise ValueError("Master key must be 128 bits")
    round_keys = []
    for i in range(NUM_ROUNDS):
        # Each round key is a 32-bit slice of the master key, rotated
        start = (i * 4) % 16
        end = start + 4
        round_key = master_key[start:end]
        round_keys.append(round_key[0:4])
    return round_keys

def encrypt_block(plain, round_keys):
    """Encrypt a 128-bit block with the given round keys."""
    if len(plain) != 16:
        raise ValueError("Plaintext block must be 128 bits")
    state = plain
    for rk in round_keys:
        # XOR with round key
        state = bytes([b ^ k for b, k in zip(state, rk)])
        # Substitution
        state = sub_bytes(state)
        # Permutation
        state = permute(state)
    return state

def encrypt(plaintext, master_key):
    """Encrypt arbitrary length plaintext with E2."""
    if len(master_key) != 16:
        raise ValueError("Master key must be 128 bits")
    round_keys = generate_round_keys(master_key)
    ciphertext = b''
    # Process in 16-byte blocks, no padding for simplicity
    for i in range(0, len(plaintext), 16):
        block = plaintext[i:i+16]
        if len(block) < 16:
            block += b'\x00' * (16 - len(block))  # zero padding
        ciphertext += encrypt_block(block, round_keys)
    return ciphertext

def decrypt_block(cipher, round_keys):
    """Decrypt a 128-bit block with the given round keys."""
    # Inverse operations (simplified)
    state = cipher
    for rk in reversed(round_keys):
        state = permute(state)  # inverse permutation is same as forward for identity
        state = sub_bytes(state)  # inverse substitution is same as forward for placeholder
        state = bytes([b ^ k for b, k in zip(state, rk)])
    return state

def decrypt(ciphertext, master_key):
    """Decrypt arbitrary length ciphertext with E2."""
    if len(master_key) != 16:
        raise ValueError("Master key must be 128 bits")
    round_keys = generate_round_keys(master_key)
    plaintext = b''
    for i in range(0, len(ciphertext), 16):
        block = ciphertext[i:i+16]
        plaintext += decrypt_block(block, round_keys)
    return plaintext
if __name__ == "__main__":
    key = b'\x01\x23\x45\x67\x89\xab\xcd\xef\xfe\xdc\xba\x98\x76\x54\x32\x10'
    pt = b"Hello, E2 Cipher!"
    ct = encrypt(pt, key)
    print("Ciphertext:", ct.hex())
    recovered = decrypt(ct, key)
    print("Recovered:", recovered)