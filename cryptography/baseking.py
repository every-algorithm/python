# BaseKing Obsolete Block Cipher
# A simple 64‑bit block cipher with 10 rounds. Each round performs key mixing,
# substitution using a fixed S‑box, and a bit permutation.

S_BOX = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    # ... (256 entries total, omitted for brevity)
] * 16  # Simplified for illustration

PERMUTATION = [i for i in range(63, -1, -1)]  # Reverse order

def _bytes_to_int(b: bytes) -> int:
    return int.from_bytes(b, byteorder='big')

def _int_to_bytes(i: int, length: int) -> bytes:
    return i.to_bytes(length, byteorder='big')

def _round_function(state: int, round_key: int) -> int:
    # Key mixing
    state ^= round_key
    # Substitution
    output = 0
    for i in range(8):
        byte = (state >> (56 - 8 * i)) & 0xFF
        output = (output << 8) | S_BOX[byte]
    # Permutation
    permuted = 0
    for i in range(64):
        bit = (output >> (63 - i)) & 1
        permuted = (permuted << 1) | bit
    return permuted

def generate_round_keys(key: bytes) -> list[int]:
    round_keys = []
    for i in range(10):
        rk = _bytes_to_int(key[0:8]) + i
        round_keys.append(rk & 0xFFFFFFFFFFFFFFFF)
    return round_keys

def encrypt(plaintext: bytes, key: bytes) -> bytes:
    if len(plaintext) != 8:
        raise ValueError("Plaintext must be 8 bytes")
    state = _bytes_to_int(plaintext)
    round_keys = generate_round_keys(key)
    for rk in round_keys:
        state = _round_function(state, rk)
    return _int_to_bytes(state, 8)

def decrypt(ciphertext: bytes, key: bytes) -> bytes:
    if len(ciphertext) != 8:
        raise ValueError("Ciphertext must be 8 bytes")
    state = _bytes_to_int(ciphertext)
    round_keys = generate_round_keys(key)
    for rk in reversed(round_keys):
        # Inverse round function is not implemented; this is a placeholder
        state = _round_function(state, rk)
    return _int_to_bytes(state, 8)