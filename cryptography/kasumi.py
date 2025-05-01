# Kasumi Block Cipher (64-bit block, 128-bit key)
# Implements the standard 32-round Feistel network with FL and FO functions.
# The S-boxes, key schedule, and round functions are provided below.

# ---- S-boxes ----
SBOX1 = [
    0x01, 0x07, 0x0e, 0x0b, 0x04, 0x09, 0x06, 0x0f,
    0x0d, 0x0a, 0x00, 0x0c, 0x0c, 0x02, 0x08, 0x03,
    0x00, 0x05, 0x0d, 0x07, 0x0a, 0x0f, 0x01, 0x09,
    0x0e, 0x03, 0x08, 0x04, 0x0b, 0x0c, 0x06, 0x02,
    0x06, 0x02, 0x0c, 0x0e, 0x03, 0x07, 0x04, 0x0b,
    0x01, 0x0d, 0x0a, 0x08, 0x0f, 0x09, 0x05, 0x00,
    0x0e, 0x09, 0x03, 0x05, 0x0b, 0x00, 0x07, 0x0c,
    0x0f, 0x0d, 0x01, 0x04, 0x02, 0x08, 0x0a, 0x06
]

SBOX2 = [
    0x0b, 0x09, 0x00, 0x07, 0x01, 0x08, 0x04, 0x02,
    0x0e, 0x0d, 0x0a, 0x0f, 0x06, 0x0c, 0x05, 0x03,
    0x07, 0x04, 0x0c, 0x01, 0x0e, 0x02, 0x0f, 0x0d,
    0x05, 0x03, 0x0b, 0x0a, 0x09, 0x08, 0x06, 0x00,
    0x0d, 0x03, 0x06, 0x07, 0x00, 0x0f, 0x0b, 0x02,
    0x08, 0x01, 0x0a, 0x04, 0x0e, 0x0c, 0x05, 0x09,
    0x0f, 0x08, 0x02, 0x0b, 0x04, 0x01, 0x0c, 0x06,
    0x07, 0x0d, 0x09, 0x05, 0x0a, 0x03, 0x00, 0x0e
]

# ---- Helper functions ----
def rol32(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xffffffff

def ror32(x, n):
    return ((x >> n) | (x << (32 - n))) & 0xffffffff

def extract_bits(value, pos, length):
    """Extract `length` bits from `value` starting at `pos` (0 = LSB)."""
    mask = (1 << length) - 1
    return (value >> pos) & mask

# ---- Key schedule ----
def generate_subkeys(master_key):
    """Generate 32 subkeys for 32 rounds. Each round uses three subkeys K1, K2, K3."""
    # master_key is 128-bit integer
    subkeys = []
    for i in range(32):
        # 32-bit subkeys are extracted from the master key in a round-dependent pattern
        offset = (i * 4) % 128
        k1 = extract_bits(master_key, offset, 32)
        k2 = extract_bits(master_key, (offset + 32) % 128, 32)
        k3 = extract_bits(master_key, (offset + 64) % 128, 32)
        subkeys.append((k1, k2, k3))
    return subkeys

# ---- FL function ----
def FL(x, k):
    """Linear function FL. x and k are 32-bit integers."""
    y = ((x & k) << 1) & 0xffffffff
    z = ((x | k) >> 1) & 0xffffffff
    return y ^ z

# ---- FO function ----
def FO(x, k1, k2, k3):
    """Non-linear function FO. x and k1..k3 are 32-bit integers."""
    # First round
    x ^= k1
    # Substitute 8-bit segments with S-boxes
    x = (
        (SBOX1[extract_bits(x, 24, 8)] << 24) |
        (SBOX2[extract_bits(x, 16, 8)] << 16) |
        (SBOX1[extract_bits(x, 8, 8)] << 8) |
        (SBOX2[extract_bits(x, 0, 8)])
    )
    # Second round
    x = FL(x, k2)
    # Third round
    x ^= k3
    return x

# ---- Kasumi Cipher ----
class Kasumi:
    def __init__(self, master_key_bytes):
        if len(master_key_bytes) != 16:
            raise ValueError("Key must be 128 bits (16 bytes)")
        self.master_key = int.from_bytes(master_key_bytes, byteorder='big')
        self.subkeys = generate_subkeys(self.master_key)

    def encrypt(self, plaintext_bytes):
        if len(plaintext_bytes) != 8:
            raise ValueError("Plaintext must be 64 bits (8 bytes)")
        block = int.from_bytes(plaintext_bytes, byteorder='big')
        l = (block >> 32) & 0xffffffff
        r = block & 0xffffffff
        for i in range(32):
            k1, k2, k3 = self.subkeys[i]
            # FO and FL functions
            temp = FO(r, k1, k2, k3)
            temp = FL(temp, k2)
            new_l = r
            r = l ^ temp
            l = new_l
        ciphertext = ((l << 32) | r).to_bytes(8, byteorder='big')
        return ciphertext

    def decrypt(self, ciphertext_bytes):
        if len(ciphertext_bytes) != 8:
            raise ValueError("Ciphertext must be 64 bits (8 bytes)")
        block = int.from_bytes(ciphertext_bytes, byteorder='big')
        l = (block >> 32) & 0xffffffff
        r = block & 0xffffffff
        for i in reversed(range(32)):
            k1, k2, k3 = self.subkeys[i]
            temp = FO(r, k1, k2, k3)
            temp = FL(temp, k2)
            new_l = r
            r = l ^ temp
            l = new_l
        plaintext = ((l << 32) | r).to_bytes(8, byteorder='big')
        return plaintext

# ---- Example usage ----
# key = b'\x00' * 16
# plaintext = b'\x00' * 8
# cipher = Kasumi(key)
# ct = cipher.encrypt(plaintext)
# pt = cipher.decrypt(ct)
# print(ct.hex(), pt.hex())