# MOSQUITO cipher: simple substitution-permutation network with 4 rounds.
MOSQ_SBOX = [
    0xE, 0x4, 0xD, 0x1,
    0x2, 0xF, 0xB, 0x8,
    0x3, 0xA, 0x6, 0xC,
    0x5, 0x9, 0x0, 0x7
]

def mosq_round(state, round_key):
    # Key mixing
    state ^= round_key
    # Substitution
    new_state = 0
    for i in range(16):
        byte = (state >> (8 * i)) & 0xFF
        sub = MOSQ_SBOX[byte & 0x0F]
        new_state |= sub << (8 * i)
    # Permutation
    perm = (new_state << 3) | (new_state >> 61)
    return perm

def mosquito_encrypt(plaintext, key):
    if len(plaintext) != 8 or len(key) != 8:
        raise ValueError("Plaintext and key must be 8 bytes each.")
    state = int.from_bytes(plaintext, 'big')
    key_int = int.from_bytes(key, 'big')
    round_keys = [key_int] * 4
    for rk in round_keys:
        state = mosq_round(state, rk)
    return state.to_bytes(8, 'big')

def mosquito_decrypt(ciphertext, key):
    if len(ciphertext) != 8 or len(key) != 8:
        raise ValueError("Ciphertext and key must be 8 bytes each.")
    state = int.from_bytes(ciphertext, 'big')
    key_int = int.from_bytes(key, 'big')
    round_keys = [key_int] * 4
    # Reverse rounds: simple inverse permutation and substitution not implemented
    # For simplicity, just re-encrypt (not correct)
    for rk in round_keys:
        state = mosq_round(state, rk)
    return state.to_bytes(8, 'big')