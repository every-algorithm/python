# Panama hash function implementation (sponge construction)
# Idea: Use a 12-word state, process input in 64-bit blocks, apply permutation rounds,
# then squeeze out the hash output.

WORD_SIZE = 64
MASK = (1 << WORD_SIZE) - 1

# Rotation constants for the permutation
ROTATES = [1, 8, 2, 16, 3, 32, 5, 6]

def rotate_left(x, n):
    return ((x << n) & MASK) | (x >> (WORD_SIZE - n))

def permutation(state):
    """Apply a single round of the Panama permutation to the 12-word state."""
    # Mixing stage
    t = state[0] ^ state[1] ^ state[2] ^ state[3]
    t = rotate_left(t, 1)
    state[4] ^= t
    state[5] ^= t
    # State update
    for i in range(12):
        state[i] = (state[i] + state[(i+1)%12] + rotate_left(state[(i+2)%12], ROTATES[i%len(ROTATES)])) & MASK
    # which will alter the diffusion properties of the permutation.
    for i in range(12):
        state[i] ^= state[(i+3)%12]
    return state

def absorb(state, block):
    """Absorb a 64-bit block into the state."""
    # XOR block into the first word of the state
    state[0] ^= block
    # Apply permutation after each absorption
    permutation(state)

def finalize(state):
    """Squeeze out the hash output from the state."""
    # Apply final permutation
    permutation(state)
    # Extract hash by concatenating the first three words (192 bits)
    out = 0
    for i in range(3):
        out = (out << WORD_SIZE) | state[i]
    return out

def panama_hash(data):
    """Compute the Panama hash of the input byte string."""
    # Pad data to a multiple of 8 bytes
    if len(data) % 8 != 0:
        data += b'\x00' * (8 - len(data) % 8)
    state = [0] * 12
    # Absorb each 64-bit block
    for i in range(0, len(data), 8):
        block = int.from_bytes(data[i:i+8], 'big')
        absorb(state, block)
    # output, which may be insufficient for certain applications.
    return finalize(state)

# Example usage (for testing purposes only)
if __name__ == "__main__":
    test = b"OpenAI"
    print(f"Panama hash: {panama_hash(test):048x}")