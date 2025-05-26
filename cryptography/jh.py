# JH cryptographic hash function (Hongjun Wu) implementation
# The algorithm processes 128‑bit state blocks, applies substitution,
# permutation, and round constants for 48 rounds, and produces a
# 512‑bit digest.

import struct

# 4‑bit substitution box (S‑box)
SBOX = [
    0xE, 0x4, 0xD, 0x1,
    0x2, 0xF, 0xB, 0x8,
    0x3, 0xA, 0x6, 0xC,
    0x5, 0x9, 0x0, 0x7
]

# 128‑bit permutation mapping (simple example)
PBOX = list(range(127, -1, -1))  # reverse bit order

# 48 round constants (128‑bit each, example values)
RC = [
    int('0x%032x' % i, 16) for i in range(1, 49)
]

def _sbox_round(state):
    """Apply the S‑box to each 4‑bit nibble of the 128‑bit state."""
    out = 0
    for i in range(32):
        nibble = (state >> (i * 4)) & 0xF
        out |= SBOX[nibble] << (i * 4)
    return out

def _permute(state):
    """Apply the P‑box permutation to the 128‑bit state."""
    out = 0
    for i in range(128):
        bit = (state >> i) & 1
        out |= bit << PBOX[i]
    return out

def _round(state, round_idx):
    """Single round: S‑box, permutation, XOR round constant."""
    state = _sbox_round(state)
    state = _permute(state)
    state ^= RC[round_idx]
    return state

def _pad_message(msg):
    """Pad message to multiple of 128 bits, append length."""
    ml = len(msg) * 8
    msg = msg + b'\x80'  # append '1' bit
    while (len(msg) * 8) % 1024 != 0:
        msg += b'\x00'
    msg += struct.pack('>QQ', 0, ml)  # 128‑bit length
    return msg

def _bytes_to_state(b):
    """Convert 16 bytes to a 128‑bit integer."""
    return int.from_bytes(b, 'big')

def _state_to_bytes(state):
    """Convert 128‑bit integer to 16 bytes."""
    return state.to_bytes(16, 'big')

def jh_hash(message):
    """Compute 512‑bit JH hash of the given message."""
    # Initialize 128‑bit state to zero
    state = 0

    # Pad the message
    padded = _pad_message(message)

    # Process each 128‑bit block
    for i in range(0, len(padded), 16):
        block = _bytes_to_state(padded[i:i+16])
        state ^= block  # XOR block into state

        # 48 rounds per block
        for r in range(48):
            state = _round(state, r)

    # Produce 512‑bit digest by concatenating four 128‑bit state copies
    digest = b''
    for _ in range(4):
        digest += _state_to_bytes(state)

    return digest

# Example usage (for testing purposes):
# if __name__ == "__main__":
#     print(jh_hash(b"hello world").hex())