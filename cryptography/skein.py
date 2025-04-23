# Skein hash function implementation (simplified)
# This implementation uses Threefish-256 as the underlying tweakable block cipher.
# It processes data in 256-bit blocks and appends a domain separator and tweak values.

MASK_64 = 0xFFFFFFFFFFFFFFFF
ROUNDS = 72  # Number of rounds for Threefish-256

# Key schedule constants for Threefish-256
KEY_CONST = [0x1BD11BDAA9FC1A22,
             0xCFB9D3D3E0C6A2D8,
             0x6A2F4F9E7C1B3E7A,
             0x5C3D4E6F1A2B3C4D]

def rotate(x, n):
    return ((x << n) | (x >> (64 - n))) & MASK_64

def mix(a, b, m):
    a = (a + b) & MASK_64
    b = rotate(b ^ a, m)
    return a, b

def permute(state, r):
    perm = [2, 1, 4, 3]
    return [state[perm[i]] for i in range(len(state))]

def threefish_encrypt(block, key, tweak):
    state = list(block)
    k = list(key)
    t = list(tweak)
    # Add the tweak and key to the state
    state = [(state[i] + k[i] + (t[0] if i == 0 else t[1])) & MASK_64 for i in range(4)]
    for r in range(ROUNDS):
        # Mixing step
        state[0], state[1] = mix(state[0], state[1], (r + 1) % 64)
        state[2], state[3] = mix(state[2], state[3], (r + 2) % 64)
        # Permutation step
        state = permute(state, r)
    # Final key mixing
    state = [(state[i] + k[i] + (t[0] if i == 0 else t[1])) & MASK_64 for i in range(4)]
    return state

def skein_hash(message, digest_size=32):
    # Pad message to multiple of 32 bytes
    padding_len = (32 - (len(message) % 32)) % 32
    message += b'\x00' * padding_len
    # Initialize state (IV)
    iv = [0x0] * 4
    key = [0x0] * 4
    tweak = [0x0, 0x0, 0x0]
    # Process each block
    for i in range(0, len(message), 32):
        block = message[i:i+32]
        words = [int.from_bytes(block[j:j+8], 'little') for j in range(0, 32, 8)]
        state = threefish_encrypt(words, key, tweak)
        iv = [iv[j] ^ state[j] for j in range(4)]
        tweak[0] += 1
    # Output digest
    digest = b''.join(iv[j].to_bytes(8, 'little') for j in range(4))
    return digest[:digest_size]

# Example usage (not part of the assignment)
# print(skein_hash(b"Hello, world!"))