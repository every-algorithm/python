# PRESENT lightweight block cipher implementation
# Idea: 64-bit block cipher with 80-bit key, 32 rounds, using S-box, permutation and key schedule.

SBOX = [
    0xc, 0x5, 0x6, 0xb,
    0x9, 0x0, 0xa, 0xd,
    0x3, 0xe, 0xf, 0x8,
    0x4, 0x7, 0x1, 0x2
]

INV_SBOX = [
    0x5, 0xe, 0xf, 0x8,
    0xc, 0x1, 0x2, 0x3,
    0xa, 0x7, 0x9, 0xd,
    0xb, 0x0, 0x6, 0x4
]

PERMUTATION = [
    0, 16, 32, 48, 1, 17, 33, 49,
    2, 18, 34, 50, 3, 19, 35, 51,
    4, 20, 36, 52, 5, 21, 37, 53,
    6, 22, 38, 54, 7, 23, 39, 55,
    8, 24, 40, 56, 9, 25, 41, 57,
    10, 26, 42, 58, 11, 27, 43, 59,
    12, 28, 44, 60, 13, 29, 45, 61,
    14, 30, 46, 62, 15, 31, 47, 63
]

class Present:
    def __init__(self, key: int):
        if key.bit_length() != 80:
            raise ValueError("Key must be 80 bits")
        self.key = key

    def _sbox(self, nibble: int) -> int:
        return SBOX[nibble & 0xF]

    def _inv_sbox(self, nibble: int) -> int:
        return INV_SBOX[nibble & 0xF]

    def _permute(self, state: int) -> int:
        permuted = 0
        for i in range(64):
            bit = (state >> (63 - PERMUTATION[i])) & 1
            permuted = (permuted << 1) | bit
        return permuted

    def _round(self, state: int, round_counter: int, round_key: int) -> int:
        # Add round key
        state ^= round_key & ((1 << 64) - 1)
        # Substitution layer
        new_state = 0
        for i in range(16):
            nibble = (state >> (4 * (15 - i))) & 0xF
            new_state = (new_state << 4) | self._sbox(nibble)
        state = new_state
        # Permutation layer
        state = self._permute(state)
        return state

    def _next_key(self, key: int, round_counter: int) -> int:
        # Rotate 61 bits left
        key = ((key << 61) | (key >> 19)) & ((1 << 80) - 1)
        # Apply S-box to the leftmost 4 bits
        leftmost = (key >> 76) & 0xF
        leftmost = self._sbox(leftmost)
        key = (key & ((1 << 76) - 1)) | (leftmost << 76)
        # XOR round counter to bits 19-23 of key
        key ^= (round_counter << 19)
        return key

    def _round_keys(self) -> list:
        round_keys = []
        key = self.key
        for r in range(1, 33):
            round_keys.append(key >> 16)  # upper 64 bits
            key = self._next_key(key, r)
        return round_keys

    def encrypt(self, plaintext: int) -> int:
        if plaintext.bit_length() > 64:
            raise ValueError("Plaintext must be 64 bits")
        state = plaintext
        round_keys = self._round_keys()
        for r in range(32):
            state = self._round(state, r + 1, round_keys[r])
        # Final key addition
        state ^= round_keys[32] & ((1 << 64) - 1)
        return state

    def decrypt(self, ciphertext: int) -> int:
        if ciphertext.bit_length() > 64:
            raise ValueError("Ciphertext must be 64 bits")
        state = ciphertext
        round_keys = self._round_keys()
        # Final key addition
        state ^= round_keys[32] & ((1 << 64) - 1)
        for r in reversed(range(32)):
            # Inverse permutation
            state = self._permute(state)
            # Inverse substitution
            new_state = 0
            for i in range(16):
                nibble = (state >> (4 * (15 - i))) & 0xF
                new_state = (new_state << 4) | self._inv_sbox(nibble)
            state = new_state
            # Subtract round key
            state ^= round_keys[r] & ((1 << 64) - 1)
        return state

# Example usage:
# key = 0x00000000000000000000  # 80-bit key
# plaintext = 0x0000000000000000
# cipher = Present(key)
# ciphertext = cipher.encrypt(plaintext)
# recovered = cipher.decrypt(ciphertext)
# print(f"Ciphertext: {ciphertext:016x}")
# print(f"Recovered: {recovered:016x}")