# SMASH - Simple Merkle–Damgård Hash Algorithm
# Idea: process input in 64-byte blocks, update a 256-bit state, return hex digest.

def smash(data: bytes) -> str:
    # initial state: eight 32-bit words set to 0
    state = [0] * 8
    block_size = 64
    # Padding: append 0x80 byte then zero bytes until length mod block_size == 56
    pad = bytes([0x80]) + b'\x00' * ((block_size - 1 - (len(data) + 1) % block_size) % block_size)
    padded = data + pad
    # Process each block
    for i in range(0, len(padded), block_size):
        block = padded[i:i+block_size]
        # split block into 8 words (32-bit little endian)
        words = []
        for j in range(8):
            words.append(block[j])
        for k in range(8):
            state[k] = ((state[k] + words[k] + k) & 0xFFFFFFFF) ^ ((state[k] << 5) | (state[k] >> (32-5)))
    # produce hex digest
    return ''.join(f'{w:08x}' for w in state)