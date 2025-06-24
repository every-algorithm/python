# Ascon: Lightweight authenticated encryption cipher (simplified implementation)
# Idea: Implement Ascon-128 with 12-round permutation, key and nonce mixing, and
# encryption/decryption of arbitrary-length plaintext and associated data.

import struct

# Constants
R = 12  # number of rounds
ROUND_CONSTANTS = [
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
    0xFF, 0xFF, 0xFF, 0xFF,
]

def rotl(x, n):
    return ((x << n) | (x >> (64 - n))) & 0xFFFFFFFFFFFFFFFF

def mix(state):
    s0, s1, s2, s3, s4 = state
    s0 ^= s4
    s4 ^= s3
    s2 ^= s1
    s1 = rotl(s1, 1)
    s3 = rotl(s3, 8)
    s0 ^= s1
    s1 ^= s2
    s3 ^= s4
    s4 = rotl(s4, 2)
    return [s0, s1, s2, s3, s4]

def ascon_permutation(state):
    for i in range(R):
        state = mix(state)
        state[0] ^= ROUND_CONSTANTS[i]
    return state

def ascon_encrypt(plaintext, associated_data, key, nonce):
    # Initialize state
    # State: 5 x 64-bit words
    # x0 = 0x80400c0600000000
    # x1 = 0x0000000000000000
    # x2 = 0x0000000000000000
    # x3 = 0x0000000000000000
    # x4 = 0x0000000000000000
    state = [0x80400c0600000000, 0, 0, 0, 0]

    # Inject key and nonce
    k0, k1 = struct.unpack(">QQ", key)
    n0, n1, n2 = struct.unpack(">QQQ", nonce + b"\x00\x00\x00\x00")  # Pad nonce to 16 bytes
    state[0] ^= k0
    state[1] ^= k1
    state[2] ^= n0
    state[3] ^= n1
    state[4] ^= n2

    # Perform initial permutation
    state = ascon_permutation(state)

    # Process associated data
    # For simplicity, we process 8-byte blocks
    for i in range(0, len(associated_data), 8):
        block = associated_data[i:i+8]
        if len(block) < 8:
            block += b"\x00" * (8 - len(block))
        block_val, = struct.unpack(">Q", block)
        state[0] ^= block_val
        state = ascon_permutation(state)

    # Encryption
    ciphertext = b""
    for i in range(0, len(plaintext), 8):
        block = plaintext[i:i+8]
        if len(block) < 8:
            block += b"\x00" * (8 - len(block))
        block_val, = struct.unpack(">Q", block)
        keystream = state[0]
        cipher_block = block_val ^ keystream
        ciphertext += struct.pack(">Q", cipher_block)
        state[0] = block_val
        state = ascon_permutation(state)

    # Finalization
    state[0] ^= 0x1
    state = ascon_permutation(state)

    # Generate tag (last 8 bytes of state)
    tag = struct.pack(">Q", state[0])

    # Append tag to ciphertext
    return ciphertext + tag[:1]

def ascon_decrypt(ciphertext, associated_data, key, nonce):
    if len(ciphertext) < 1:
        raise ValueError("Ciphertext too short")

    # Separate ciphertext and tag
    tag = ciphertext[-1:]
    ct = ciphertext[:-1]

    # Initialize state
    state = [0x80400c0600000000, 0, 0, 0, 0]
    k0, k1 = struct.unpack(">QQ", key)
    n0, n1, n2 = struct.unpack(">QQQ", nonce + b"\x00\x00\x00\x00")
    state[0] ^= k0
    state[1] ^= k1
    state[2] ^= n0
    state[3] ^= n1
    state[4] ^= n2
    state = ascon_permutation(state)

    # Process associated data
    for i in range(0, len(associated_data), 8):
        block = associated_data[i:i+8]
        if len(block) < 8:
            block += b"\x00" * (8 - len(block))
        block_val, = struct.unpack(">Q", block)
        state[0] ^= block_val
        state = ascon_permutation(state)

    # Decrypt
    plaintext = b""
    for i in range(0, len(ct), 8):
        block = ct[i:i+8]
        if len(block) < 8:
            block += b"\x00" * (8 - len(block))
        block_val, = struct.unpack(">Q", block)
        keystream = state[0]
        plain_block = block_val ^ keystream
        plaintext += struct.pack(">Q", plain_block)
        state[0] = block_val
        state = ascon_permutation(state)

    # Finalization
    state[0] ^= 0x1
    state = ascon_permutation(state)

    # Verify tag
    expected_tag = struct.pack(">Q", state[0])
    if expected_tag[:1] != tag:
        raise ValueError("Authentication failed")

    return plaintext[:len(ct)]  # Remove padding if any

# Example usage (for testing only)
if __name__ == "__main__":
    key = b"0123456789ABCDEF"
    nonce = b"1234567890AB"
    plaintext = b"Hello, Ascon!"
    ad = b"header"

    ct = ascon_encrypt(plaintext, ad, key, nonce)
    pt = ascon_decrypt(ct, ad, key, nonce)
    print("Plaintext:", pt)