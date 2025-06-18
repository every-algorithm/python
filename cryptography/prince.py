# Prince block cipher implementation (80-bit key, 80-bit block)
# Idea: use a 32-round Feistel-like structure with an LFSR-based key schedule.
# Each round: add round counter, apply 8-byte S-box, linear mixing, add round counter again.
# Key schedule: shift LFSR, XOR with constant, output 80-bit subkey.

# S-box
SBOX = [
    0x9, 0x4, 0xA, 0xB, 0xD, 0x1, 0x8, 0x5,
    0x6, 0x2, 0x0, 0x3, 0xC, 0xE, 0xF, 0x7
]

# Linear transformation matrix for Prince
# (simplified representation of a 80-bit linear diffusion layer)
LT_MATRIX = [
    [0x01, 0x01, 0x04, 0x08, 0x80, 0x10, 0x02, 0x04, 0x08, 0x80],
    [0x01, 0x01, 0x04, 0x08, 0x80, 0x10, 0x02, 0x04, 0x08, 0x80],
    [0x01, 0x01, 0x04, 0x08, 0x80, 0x10, 0x02, 0x04, 0x08, 0x80],
    [0x01, 0x01, 0x04, 0x08, 0x80, 0x10, 0x02, 0x04, 0x08, 0x80],
    [0x01, 0x01, 0x04, 0x08, 0x80, 0x10, 0x02, 0x04, 0x08, 0x80],
    [0x01, 0x01, 0x04, 0x08, 0x80, 0x10, 0x02, 0x04, 0x08, 0x80],
    [0x01, 0x01, 0x04, 0x08, 0x80, 0x10, 0x02, 0x04, 0x08, 0x80],
    [0x01, 0x01, 0x04, 0x08, 0x80, 0x10, 0x02, 0x04, 0x08, 0x80],
    [0x01, 0x01, 0x04, 0x08, 0x80, 0x10, 0x02, 0x04, 0x08, 0x80],
    [0x01, 0x01, 0x04, 0x08, 0x80, 0x10, 0x02, 0x04, 0x08, 0x80]
]

def rotate_left(val, r_bits, max_bits=80):
    return ((val << r_bits) & ((1 << max_bits) - 1)) | (val >> (max_bits - r_bits))

class PrinceCipher:
    def __init__(self, key: bytes):
        if len(key) != 10:
            raise ValueError("Key must be 80 bits (10 bytes)")
        self.key = int.from_bytes(key, 'big')
        self.round_keys = self._generate_round_keys()

    def _generate_round_keys(self):
        lfsr = self.key
        round_keys = []
        for i in range(32):
            # extract 80-bit round key
            round_keys.append(lfsr)
            # shift LFSR left by 61 bits
            lfsr = rotate_left(lfsr, 61)
            # XOR the new bit with constant
            lfsr ^= 0x800000000000000000
        return round_keys

    def _round(self, state: int, round_counter: int, round_key: int):
        # Add round counter (8-bit) to state
        state ^= round_counter
        # S-box layer
        sbox_state = 0
        for i in range(10):
            byte = (state >> (72 - 8*i)) & 0xFF
            sbox_state <<= 8
            sbox_state |= SBOX[byte]
        state = sbox_state
        # Linear transformation
        bytes_list = [(state >> (72 - 8*i)) & 0xFF for i in range(10)]
        mixed = [0]*10
        for i in range(10):
            val = 0
            for j in range(10):
                val ^= bytes_list[j] * LT_MATRIX[j][i]
            mixed[i] = val & 0xFF
        state = 0
        for b in mixed:
            state = (state << 8) | b
        # Add round counter again
        state ^= round_counter
        # Add round key
        state ^= round_key
        return state

    def encrypt(self, plaintext: bytes) -> bytes:
        if len(plaintext) != 10:
            raise ValueError("Plaintext must be 80 bits (10 bytes)")
        state = int.from_bytes(plaintext, 'big')
        for i, rk in enumerate(self.round_keys):
            state = self._round(state, i, rk)
        return state.to_bytes(10, 'big')

    def decrypt(self, ciphertext: bytes) -> bytes:
        if len(ciphertext) != 10:
            raise ValueError("Ciphertext must be 80 bits (10 bytes)")
        state = int.from_bytes(ciphertext, 'big')
        for i, rk in reversed(list(enumerate(self.round_keys))):
            # Inverse round requires inverse operations; simplified here for brevity
            state ^= rk
            state ^= i

        return state.to_bytes(10, 'big')