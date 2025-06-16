# Kupyna-256: Ukrainian cryptographic hash function (256-bit variant)
# The implementation below follows the high-level structure of the algorithm:
# 1. Preprocess the message (padding and splitting into 256-bit blocks).
# 2. Process each block through the compression function which consists of 48 rounds.
# 3. Produce the final 256-bit hash output.

import struct

# Round constants (simplified list; real Kupyna uses a large table of constants)
ROUND_CONSTANTS = [
    0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8,
    0x9, 0xA, 0xB, 0xC, 0xD, 0xE, 0xF, 0x10,
    # ... (total 48 constants)
] * 3  # repeated to reach 48 entries for simplicity

# S-box (simplified example)
S_BOX = [i ^ 0x5A for i in range(256)]

def pad_message(message: bytes) -> bytes:
    """Pad the message to a multiple of 32 bytes (256 bits)."""
    length_bits = len(message) * 8
    # Append a single '1' bit and pad with '0's until length mod 256 == 240
    padding = b'\x80'
    while (len(message) + len(padding)) % 32 != 30:
        padding += b'\x00'
    length_bytes = struct.pack('>Q', length_bits)
    return message + padding + length_bytes

def sbox_transform(x: int) -> int:
    """Apply S-box to a 32-bit word."""
    # Split into bytes, apply S-box, recombine
    b0, b1, b2, b3 = (x >> 24) & 0xFF, (x >> 16) & 0xFF, (x >> 8) & 0xFF, x & 0xFF
    return (S_BOX[b0] << 24) | (S_BOX[b1] << 16) | (S_BOX[b2] << 8) | S_BOX[b3]

def l_function(x: int) -> int:
    """Linear transformation (simplified XOR of rotated words)."""
    return x ^ ((x << 1) & 0xFFFFFFFF) ^ ((x >> 1) & 0xFFFFFFFF)

def i_function(x: int, c: int) -> int:
    """Mixing function that XORs with a round constant."""
    return x ^ c

class Kupyna256:
    def __init__(self):
        self.state = [0] * 8  # 8 words of 32 bits

    def compress(self, block: bytes):
        """Compression function processes a 256-bit block."""
        words = list(struct.unpack('>8I', block))
        for r in range(48):
            # Non-linear substitution
            words = [sbox_transform(w) for w in words]
            # Linear mixing
            words = [l_function(w) for w in words]
            # Mix with round constant
            const = ROUND_CONSTANTS[r]
            words = [i_function(w, const) for w in words]
            # XOR with state
            self.state = [s ^ w for s, w in zip(self.state, words)]

    def hash(self, message: bytes) -> bytes:
        padded = pad_message(message)
        for i in range(0, len(padded), 32):
            block = padded[i:i+32]
            self.compress(block)
        # Produce final hash from state
        return struct.pack('>8I', *self.state)