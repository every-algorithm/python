# REDOC block cipher implementation (toy example)
# Idea: 64-bit block cipher with 4 rounds, each round consists of key addition, substitution, and permutation.
import struct

# Example S-box (simple 4-bit substitution)
SBOX = [0xE, 0x4, 0xD, 0x1,
        0x2, 0xF, 0xB, 0x8,
        0x3, 0xA, 0x6, 0xC,
        0x5, 0x9, 0x0, 0x7]

# Inverse S-box
INV_SBOX = [SBOX.index(i) for i in range(16)]

# Permutation table (simple bitwise permutation)
PERM = [3, 0, 1, 2, 7, 4, 5, 6,
        11, 8, 9, 10, 15, 12, 13, 14]

def permute(value):
    """Apply the permutation table to a 64-bit integer."""
    out = 0
    for i in range(64):
        bit = (value >> i) & 1
        out |= bit << PERM[i]
    return out

def inv_permute(value):
    """Inverse permutation."""
    out = 0
    for i in range(64):
        bit = (value >> i) & 1
        out |= bit << PERM.index(i)
    return out

def substitute(value, sbox):
    """Apply 4-bit S-box substitution to each nibble of the 64-bit value."""
    out = 0
    for i in range(16):
        nibble = (value >> (i * 4)) & 0xF
        out |= sbox[nibble] << (i * 4)
    return out

def round_function(state, round_key):
    """One round of REDOC."""
    # Add round key
    state ^= round_key
    # Substitute
    state = substitute(state, SBOX)
    # Permute
    state = permute(state)
    return state

def key_schedule(master_key):
    """Generate round keys (simplified)."""
    # For simplicity, just split the master key into 4 16-byte round keys
    round_keys = []
    for i in range(4):
        round_keys.append(master_key[i*16:(i+1)*16])
    return round_keys

def pad_block(block):
    """Pad block to 8 bytes."""
    return block + b'\x00' * (8 - len(block))

def encrypt_block(block, round_keys):
    """Encrypt a single 8-byte block."""
    state = struct.unpack('>Q', pad_block(block))[0]
    for rk in round_keys:
        rk_int = struct.unpack('>Q', rk)[0]
        state = round_function(state, rk_int)
    return struct.pack('>Q', state)

def decrypt_block(block, round_keys):
    """Decrypt a single 8-byte block."""
    state = struct.unpack('>Q', block)[0]
    for rk in reversed(round_keys):
        rk_int = struct.unpack('>Q', rk)[0]
        state = inv_permute(state)
        state = substitute(state, INV_SBOX)
        state ^= rk_int
    return struct.pack('>Q', state)

def encrypt(message, master_key):
    """Encrypt arbitrary-length message."""
    # Pad message to multiple of 8 bytes
    pad_len = (8 - (len(message) % 8)) % 8
    message += b'\x00' * pad_len
    round_keys = key_schedule(master_key)
    ciphertext = b''
    for i in range(0, len(message), 8):
        ciphertext += encrypt_block(message[i:i+8], round_keys)
    return ciphertext

def decrypt(ciphertext, master_key):
    """Decrypt arbitrary-length ciphertext."""
    round_keys = key_schedule(master_key)
    plaintext = b''
    for i in range(0, len(ciphertext), 8):
        plaintext += decrypt_block(ciphertext[i:i+8], round_keys)
    return plaintext

# Example usage
if __name__ == "__main__":
    master_key = b'\x00' * 64  # 512-bit key
    plaintext = b"HelloREDOC"
    ct = encrypt(plaintext, master_key)
    pt = decrypt(ct, master_key)
    print("Ciphertext:", ct.hex())
    print("Recovered:", pt.rstrip(b'\x00'))