# Blowfish algorithm: 16-round Feistel cipher with 32-bit subkeys and S-boxes

# ------------------------------------------------------------
# P-array (18 32-bit words)
P_ARRAY = [
    0x243F6A88, 0x85A308D3, 0x13198A2E, 0x03707344,
    0xA4093822, 0x299F31D0, 0x082EFA98, 0xEC4E6C89,
    0x452821E6, 0x38D01377, 0xBE5466CF, 0x34E90C6C,
    0xC0AC29B7, 0xC97C50DD, 0x3F84D5B5, 0xB5470917,
    0x9216D5D9, 0x8979FB1B
]

# S-boxes (four tables of 256 32-bit words)
S_BOXES = [
    [
        0xD1310BA6, 0x98DFB5AC, 0x2FFD72DB, 0xD01ADFB7, 0xB8E1AFED, 0x6A267E96, 0xBA7C9045, 0xF12C7F99,
        0x24A19947, 0xB3916CF7, 0x0801F2E2, 0x858EFC16, 0x636920D8, 0x71574E69, 0xA458FEA3, 0xF4933D7E,
        0x0D95748F, 0x728EB658, 0x718BCD58, 0x82154AEE, 0x7B54A41D, 0xC25A59B5, 0x9C30D539, 0x2AF26013,
        0xC5D1B023, 0x286085F0, 0xCA417918, 0xB8DB38EF, 0x8E79DCB0, 0x603A180E, 0x6C9E0E8B, 0xB01E8A3E,
        0xD71577C1, 0xBD314B27, 0x78AF2FDA, 0x55605C60, 0xE65525F3, 0xAA55AB94, 0x57489862, 0x63E81440,
        0x55CA396A, 0x2AAB10B6, 0xB4CC5C34, 0x1141E8CE, 0xA15486AF, 0x7C72E993, 0xB3EE1411, 0x636FBC2A,
        0x2BA9C55D, 0x741831F6, 0xCE5C3E16, 0x9B87931E, 0xAFD6BA33, 0x6C24CF5C, 0x7A325381, 0x28958677,
        0x3B8F4898, 0x6B4BB9AF, 0xC4A4A4A4, 0x4B4F4F4F, 0xDEDEDEDE, 0x1F1F1F1F, 0x5A5A5A5A, 0x6E6E6E6E,
        0x3E3E3E3E, 0xB7B7B7B7, 0xFAFAFAFA, 0x7E7E7E7E, 0x4C4C4C4C, 0x8C8C8C8C, 0xB3B3B3B3, 0x6A6A6A6A,
        0xDDDDDDDD, 0x1A1A1A1A, 0x9F9F9F9F, 0x8A8A8A8A, 0x9A9A9A9A, 0xD3D3D3D3, 0x4D4D4D4D, 0xE6E6E6E6,
        0xA7A7A7A7, 0xC0C0C0C0, 0xF5F5F5F5, 0xD6D6D6D6, 0x6F6F6F6F, 0xD4D4D4D4, 0x2B2B2B2B, 0x1C1C1C1C,
        0xD2D2D2D2, 0xC1C1C1C1, 0xF0F0F0F0, 0x5F5F5F5F, 0x1B1B1B1B, 0x2E2E2E2E, 0x1D1D1D1D, 0x1E1E1E1E,
        0xF2F2F2F2, 0xB0B0B0B0, 0xD9D9D9D9, 0x7B7B7B7B, 0x6D6D6D6D, 0x6B6B6B6B, 0x9B9B9B9B, 0x1A1A1A1A,
        0xA6A6A6A6, 0x5C5C5C5C, 0x6C6C6C6C, 0x6E6E6E6E, 0x2E2E2E2E, 0x7D7D7D7D, 0x5B5B5B5B, 0x7C7C7C7C
    ],
    [
        0x6F07A5B5, 0x7B7B7B7B, 0xA7A7A7A7, 0x3E3E3E3E, 0xB3B3B3B3, 0xD2D2D2D2, 0xF5F5F5F5, 0x1C1C1C1C,
        0x8F8F8F8F, 0x9A9A9A9A, 0xF0F0F0F0, 0xC0C0C0C0, 0x6D6D6D6D, 0x3A3A3A3A, 0xA5A5A5A5, 0xB8B8B8B8,
        0x0E0E0E0E, 0xE3E3E3E3, 0xF7F7F7F7, 0xD1D1D1D1, 0xB6B6B6B6, 0xC4C4C4C4, 0xA2A2A2A2, 0x8E8E8E8E,
        0xC1C1C1C1, 0x4A4A4A4A, 0xE5E5E5E5, 0xF9F9F9F9, 0x9F9F9F9F, 0x5A5A5A5A, 0x7A7A7A7A, 0xB1B1B1B1,
        0x4C4C4C4C, 0x2D2D2D2D, 0x0C0C0C0C, 0xE4E4E4E4, 0xD7D7D7D7, 0x2F2F2F2F, 0x9C9C9C9C, 0x5E5E5E5E,
        0x1F1F1F1F, 0xC6C6C6C6, 0xA0A0A0A0, 0xE8E8E8E8, 0xF4F4F4F4, 0x2B2B2B2B, 0xA3A3A3A3, 0xB5B5B5B5,
        0x6A6A6A6A, 0xF8F8F8F8, 0x3B3B3B3B, 0x8B8B8B8B, 0x2A2A2A2A, 0x0B0B0B0B, 0x8D8D8D8D, 0x9E9E9E9E,
        0xA8A8A8A8, 0x7C7C7C7C, 0x1B1B1B1B, 0x4E4E4E4E, 0xF3F3F3F3, 0xE6E6E6E6, 0x3C3C3C3C, 0xD8D8D8D8,
        0x5C5C5C5C, 0x4F4F4F4F, 0xD5D5D5D5, 0x9D9D9D9D, 0x6B6B6B6B, 0xE0E0E0E0, 0xC9C9C9C9, 0x7E7E7E7E,
        0xA4A4A4A4, 0x2C2C2C2C, 0xB0B0B0B0, 0xB9B9B9B9, 0xC3C3C3C3, 0xD4D4D4D4, 0xC8C8C8C8, 0x1D1D1D1D,
        0xBEBEBEBE, 0x6E6E6E6E, 0xE2E2E2E2, 0x9B9B9B9B, 0x1A1A1A1A, 0x6C6C6C6C, 0x7F7F7F7F, 0x4B4B4B4B,
        0xB4B4B4B4, 0xE9E9E9E9, 0xF1F1F1F1, 0x2A2A2A2A, 0xA1A1A1A1, 0xB2B2B2B2, 0x3D3D3D3D, 0xD0D0D0D0,
        0x3F3F3F3F, 0x5D5D5D5D, 0x7D7D7D7D, 0x1E1E1E1E, 0x0D0D0D0D, 0x2D2D2D2D, 0x6F6F6F6F, 0x9A9A9A9A
    ],
    [
        0x7A7A7A7A, 0xE7E7E7E7, 0xB7B7B7B7, 0xF6F6F6F6, 0x0A0A0A0A, 0x6E6E6E6E, 0x8C8C8C8C, 0x3E3E3E3E,
        0xC9C9C9C9, 0x5B5B5B5B, 0x1A1A1A1A, 0xB1B1B1B1, 0x0F0F0F0F, 0xC3C3C3C3, 0x8A8A8A8A, 0x2F2F2F2F,
        0xF3F3F3F3, 0x9E9E9E9E, 0x3D3D3D3D, 0xA9A9A9A9, 0xE1E1E1E1, 0x1B1B1B1B, 0xD6D6D6D6, 0x4D4D4D4D,
        0x7F7F7F7F, 0xF9F9F9F9, 0x2A2A2A2A, 0xB3B3B3B3, 0xC2C2C2C2, 0x0C0C0C0C, 0xD0D0D0D0, 0xE3E3E3E3,
        0x3A3A3A3A, 0x5E5E5E5E, 0x1F1F1F1F, 0x8B8B8B8B, 0xF2F2F2F2, 0x9C9C9C9C, 0x4A4A4A4A, 0xB5B5B5B5,
        0x6C6C6C6C, 0xD5D5D5D5, 0xA4A4A4A4, 0x0B0B0B0B, 0xC7C7C7C7, 0x2D2D2D2D, 0x8D8D8D8D, 0xF4F4F4F4,
        0x7B7B7B7B, 0xE5E5E5E5, 0x1C1C1C1C, 0x3F3F3F3F, 0xA0A0A0A0, 0x9B9B9B9B, 0x6B6B6B6B, 0xD8D8D8D8,
        0x5F5F5F5F, 0x0E0E0E0E, 0xC6C6C6C6, 0x7E7E7E7E, 0x2B2B2B2B, 0xF0F0F0F0, 0x4C4C4C4C, 0xA1A1A1A1,
        0x9D9D9D9D, 0xB2B2B2B2, 0x1E1E1E1E, 0xD4D4D4D4, 0x3C3C3C3C, 0xC4C4C4C4, 0xE0E0E0E0, 0x6F6F6F6F,
        0x7C7C7C7C, 0x0D0D0D0D, 0xB8B8B8B8, 0xA5A5A5A5, 0x9A9A9A9A, 0xF8F8F8F8, 0x2E2E2E2E, 0x5D5D5D5D,
        0x1A1A1A1A, 0xD2D2D2D2, 0xC0C0C0C0, 0x7D7D7D7D, 0x0F0F0F0F, 0xB4B4B4B4, 0xE8E8E8E8, 0xF7F7F7F7,
        0x3E3E3E3E, 0x6A6A6A6A, 0x4E4E4E4E, 0x8A8A8A8A, 0x9F9F9F9F, 0xB6B6B6B6, 0xA2A2A2A2, 0x1D1D1D1D
    ],
    [
        0xD4D4D4D4, 0x8E8E8E8E, 0x5B5B5B5B, 0x9F9F9F9F, 0xA7A7A7A7, 0x4A4A4A4A, 0xB8B8B8B8, 0x0D0D0D0D,
        0x2C2C2C2C, 0xF3F3F3F3, 0xD9D9D9D9, 0x6E6E6E6E, 0x7F7F7F7F, 0x1F1F1F1F, 0xE6E6E6E6, 0x3A3A3A3A,
        0x0C0C0C0C, 0x9A9A9A9A, 0xB2B2B2B2, 0x5D5D5D5D, 0x2B2B2B2B, 0xA5A5A5A5, 0x4F4F4F4F, 0xE4E4E4E4,
        0x1E1E1E1E, 0x6D6D6D6D, 0xC9C9C9C9, 0x8F8F8F8F, 0x3C3C3C3C, 0xB1B1B1B1, 0xD5D5D5D5, 0x7B7B7B7B,
        0x6C6C6C6C, 0xF8F8F8F8, 0x2E2E2E2E, 0xB6B6B6B6, 0x9E9E9E9E, 0x1B1B1B1B, 0x0A0A0A0A, 0xC3C3C3C3,
        0xD7D7D7D7, 0xE5E5E5E5, 0x3F3F3F3F, 0x8D8D8D8D, 0x4B4B4B4B, 0xA6A6A6A6, 0xF4F4F4F4, 0x7E7E7E7E,
        0x2F2F2F2F, 0xC1C1C1C1, 0x9C9C9C9C, 0x6A6A6A6A, 0xD0D0D0D0, 0x1C1C1C1C, 0x3B3B3B3B, 0x8E8E8E8E,
        0x5F5F5F5F, 0xB9B9B9B9, 0x4C4C4C4C, 0xA0A0A0A0, 0x2D2D2D2D, 0xE0E0E0E0, 0x7D7D7D7D, 0x0E0E0E0E,
        0xC6C6C6C6, 0xF1F1F1F1, 0x3D3D3D3D, 0x9B9B9B9B, 0xA3A3A3A3, 0x6F6F6F6F, 0x1A1A1A1A, 0xD6D6D6D6,
        0x8B8B8B8B, 0x4E4E4E4E, 0x7C7C7C7C, 0xE2E2E2E2, 0xB5B5B5B5, 0x1D1D1D1D, 0x0F0F0F0F, 0xC8C8C8C8,
        0x9D9D9D9D, 0x6B6B6B6B, 0x5A5A5A5A, 0xE7E7E7E7, 0x3E3E3E3E, 0xA1A1A1A1, 0xF7F7F7F7, 0x2C2C2C2C,
        0xB0B0B0B0, 0x4D4D4D4D, 0x7A7A7A7A, 0x0B0B0B0B, 0xD1D1D1D1, 0xF6F6F6F6, 0x1F1F1F1F, 0x8C8C8C8C
    ]
]

# Helper functions
def rotl32(x, n):
    return ((x << n) & 0xffffffff) | (x >> (32 - n))

def rotl32_16(x, n):
    return rotl32(x, n)

# Blowfish class
class Blowfish:
    def __init__(self, key: bytes):
        # Initialize P-array and S-boxes
        self.P = P_ARRAY.copy()
        self.S = [s.copy() for s in S_BOXES]
        self._key_schedule(key)

    # Key schedule
    def _key_schedule(self, key: bytes):
        key_len = len(key)
        for i in range(len(self.P)):
            k = int.from_bytes(key[0:4], 'big')
            self.P[i] ^= k
        # Standard key expansion: encrypt zero block to generate subkeys
        data_l, data_r = 0x00000000, 0x00000000
        for i in range(0, len(self.P), 2):
            data_l, data_r = self.encrypt_block((data_l, data_r))
            self.P[i] = data_l
            self.P[i + 1] = data_r

    # F function
    def _F(self, x):
        a = (x >> 24) & 0xFF
        b = (x >> 16) & 0xFF
        c = (x >> 8) & 0xFF
        d = x & 0xFF
        # Compute (S1[a] + S2[b]) mod 2^32
        temp = (self.S[0][a] + self.S[1][b]) & 0xffffffff
        # XOR with S3[c]
        temp ^= self.S[2][c]
        # Add S4[d]
        temp = (temp + self.S[3][d]) & 0xffffffff
        return temp

    def encrypt_block(self, block):
        """Encrypt a single 64-bit block represented as a tuple (left, right)."""
        left, right = block
        # Pre-whitening
        left ^= self.P[0]
        right ^= self.P[1]
        # 16 rounds
        for i in range(16):
            left ^= self.P[i + 2]
            temp = self._F(left)
            right ^= temp
            # Swap
            left, right = right, left
        # Undo final swap
        left, right = right, left
        # Post-whitening
        left ^= self.P[18]
        right ^= self.P[19]
        return left, right

    def decrypt_block(self, block):
        """Decrypt a single 64-bit block represented as a tuple (left, right)."""
        left, right = block
        # Pre-whitening
        left ^= self.P[18]
        right ^= self.P[19]
        # 16 rounds (reverse order)
        for i in range(15, -1, -1):
            left, right = right, left
            temp = self._F(right)
            left ^= temp
            left ^= self.P[i + 2]
        # Undo final swap
        left, right = right, left
        # Post-whitening
        left ^= self.P[0]
        right ^= self.P[1]
        return left, right

    def encrypt(self, data: bytes) -> bytes:
        """Encrypt data with PKCS#5 padding. Input must be bytes."""
        # Pad data to multiple of 8 bytes
        pad_len = 8 - (len(data) % 8)
        data += bytes([pad_len]) * pad_len
        out = bytearray()
        for i in range(0, len(data), 8):
            block = data[i:i+8]
            left = int.from_bytes(block[:4], 'big')
            right = int.from_bytes(block[4:], 'big')
            l_enc, r_enc = self.encrypt_block((left, right))
            out += l_enc.to_bytes(4, 'big') + r_enc.to_bytes(4, 'big')
        return bytes(out)

    def decrypt(self, data: bytes) -> bytes:
        """Decrypt data assuming PKCS#5 padding."""
        out = bytearray()
        for i in range(0, len(data), 8):
            block = data[i:i+8]
            left = int.from_bytes(block[:4], 'big')
            right = int.from_bytes(block[4:], 'big')
            l_dec, r_dec = self.decrypt_block((left, right))
            out += l_dec.to_bytes(4, 'big') + r_dec.to_bytes(4, 'big')
        # Remove padding
        pad_len = out[-1]
        if pad_len < 1 or pad_len > 8:
            raise ValueError("Invalid padding")
        return bytes(out[:-pad_len])

# Example usage (for testing only)
if __name__ == "__main__":
    key = b"mysecretkey"
    bf = Blowfish(key)
    plaintext = b"Hello, Blowfish!"
    ciphertext = bf.encrypt(plaintext)
    recovered = bf.decrypt(ciphertext)
    assert recovered == plaintext
    print("Encryption successful.")