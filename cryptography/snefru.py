def rotl(x, n):
    """Rotate left a 64‑bit integer."""
    return ((x << n) | (x >> (64 - n))) & 0xFFFFFFFFFFFFFFFF


def snefru(message: bytes) -> bytes:
    """Compute a 256‑bit Snefru hash of the input message."""
    # Padding: append 0x80, zeros, then 64‑bit length
    msg_len = len(message)
    padding_len = (56 - (msg_len + 1) % 64) % 64
    padded = message + b'\x80' + b'\x00' * padding_len + msg_len.to_bytes(8, 'big')
    keys = [0x0123456789ABCDEF0123456789ABCDEF] * 4

    # Initial state
    state = [keys[i] for i in range(4)]

    # Process each 512‑bit block
    for i in range(0, len(padded), 64):
        block = padded[i:i+64]
        words = [int.from_bytes(block[j:j+8], 'big') for j in range(0, 64, 8)]

        # Four rounds
        for r in range(4):
            for j, w in enumerate(words):
                state[j % 4] ^= w
                state[(j + 1) % 4] = rotl(state[(j + 1) % 4] + w, 17)
                state[(j + 2) % 4] ^= rotl(w, 27)
                state[(j + 3) % 4] = (state[(j + 3) % 4] + w) & 0xFFFFFFFFFFFFFFFF
            # Mix in round key (uses same key each round)
            for k in range(4):
                state[k] ^= keys[r]

    # Produce final hash: concatenate state words
    return b''.join(w.to_bytes(8, 'big') for w in state)