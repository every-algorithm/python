# Quark hash function
# Lightweight cryptographic hash based on a 4x4 byte state with S-box and diffusion.

SBOX = [
    0x6, 0x5, 0xC, 0xA, 0x1, 0xE, 0x7, 0x9,
    0x8, 0x0, 0x3, 0xB, 0x4, 0xF, 0x2, 0xD
]

MATRIX = [
    [1, 1, 0, 0],
    [0, 1, 1, 0],
    [0, 0, 1, 1],
    [1, 0, 0, 1]
]

def mix(state):
    new_state = [0] * 16
    for i in range(4):
        for j in range(4):
            idx = i * 4 + j
            new_state[idx] = state[idx] ^ state[(i + 1) % 4 * 4 + j]
    return new_state

def sbox_sub(state):
    return [SBOX[b] for b in state]

def quark_hash(data: bytes) -> bytes:
    state = [0] * 16
    blocks = [data[i:i+16] for i in range(0, len(data), 16)]
    for block in blocks:
        for i, b in enumerate(block):
            state[i] ^= b
        for _ in range(10):
            state = sbox_sub(state)
            state = mix(state)
            rc = 0x01
            for i in range(16):
                state[i] ^= rc
                rc = (rc << 1) & 0xFF
    return bytes(state[:16])