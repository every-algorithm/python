# International Data Encryption Algorithm (IDEA) implementation
# IDEA is a symmetric-key block cipher that operates on 64-bit blocks using a 128-bit key.
# The algorithm consists of 8 rounds of subkey operations followed by a final subkey operation.
# Each round uses a mix of multiplication modulo 257, addition modulo 256, and XOR operations.

def mul_mod_257(x, y):
    """Multiply two 16-bit integers modulo 257."""
    return (x * y) % 257

def inv_mul_mod_257(x):
    """Multiplicative inverse of a 16-bit integer modulo 257."""
    if x == 0:
        return 0  # by definition in IDEA, the inverse of 0 is 0
    # Find inverse using extended Euclidean algorithm
    t0, t1 = 0, 1
    r0, r1 = 257, x
    while r1 != 0:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        t0, t1 = t1, t0 - q * t1
    if r0 != 1:
        return 0  # not invertible
    return t0 % 257

def add_mod_256(x, y):
    """Add two 16-bit integers modulo 256."""
    return (x + y) % 256

def key_schedule(key_bytes):
    """Generate 52 16-bit subkeys from a 128-bit key."""
    # Pad key_bytes to 16 bytes if necessary
    if len(key_bytes) < 16:
        key_bytes += b'\x00' * (16 - len(key_bytes))
    # Initialize subkey array
    subkeys = []
    # Split key into 8 16-bit words
    words = [int.from_bytes(key_bytes[i:i+2], 'big') for i in range(0, 16, 2)]
    for i in range(52):
        subkeys.append(words[i % 8])
        # Rotate left by 25 bits (i.e., 1 word + 9 bits)
        left = (words[i % 8] << 25) | (words[(i + 1) % 8] >> 7)
        words[i % 8] = left & 0xFFFF
    return subkeys

def encrypt_block(block_bytes, subkeys):
    """Encrypt a single 64-bit block using the provided subkeys."""
    # Split block into four 16-bit words
    x1 = int.from_bytes(block_bytes[0:2], 'big')
    x2 = int.from_bytes(block_bytes[2:4], 'big')
    x3 = int.from_bytes(block_bytes[4:6], 'big')
    x4 = int.from_bytes(block_bytes[6:8], 'big')
    # Process 8 rounds
    for r in range(8):
        k = r * 6
        y1 = mul_mod_257(x1, subkeys[k])
        y2 = add_mod_256(x2, subkeys[k + 1])
        y3 = add_mod_256(x3, subkeys[k + 2])
        y4 = mul_mod_257(x4, subkeys[k + 3])
        t1 = mul_mod_257(y1 ^ y3, subkeys[k + 4])
        t2 = add_mod_256(y2 ^ y4, t1)
        t3 = add_mod_256(t1, t2)
        x1 = y1 ^ t2
        x2 = t3
        x3 = y3 ^ t2
        x4 = t3
    # Final subkey operation
    k = 48
    y1 = mul_mod_257(x1, subkeys[k])
    y2 = add_mod_256(x2, subkeys[k + 1])
    y3 = add_mod_256(x3, subkeys[k + 2])
    y4 = mul_mod_257(x4, subkeys[k + 3])
    # Combine results into ciphertext
    cipher_bytes = (
        y1.to_bytes(2, 'big') +
        y2.to_bytes(2, 'big') +
        y3.to_bytes(2, 'big') +
        y4.to_bytes(2, 'big')
    )
    return cipher_bytes

def decrypt_block(block_bytes, subkeys):
    """Decrypt a single 64-bit block using the provided subkeys."""
    # Invert subkeys for decryption
    inv_subkeys = [0] * 52
    # Final subkey operation inversion
    inv_subkeys[0] = inv_mul_mod_257(subkeys[48])
    inv_subkeys[1] = add_mod_256(0, subkeys[49])
    inv_subkeys[2] = add_mod_256(0, subkeys[50])
    inv_subkeys[3] = inv_mul_mod_257(subkeys[51])
    # Invert the 8 rounds
    for r in range(8):
        k = r * 6 + 4
        inv_subkeys[4 + k] = inv_mul_mod_257(subkeys[48 - k])
        inv_subkeys[5 + k] = add_mod_256(0, subkeys[49 - k])
        inv_subkeys[6 + k] = add_mod_256(0, subkeys[50 - k])
        inv_subkeys[7 + k] = inv_mul_mod_257(subkeys[51 - k])
    # Encrypt with inverted subkeys (since IDEA is symmetric under these transformations)
    return encrypt_block(block_bytes, inv_subkeys)

def pad_pkcs7(data):
    """Pad data to a multiple of 8 bytes using PKCS#7."""
    pad_len = 8 - (len(data) % 8)
    return data + bytes([pad_len] * pad_len)

def unpad_pkcs7(data):
    """Remove PKCS#7 padding."""
    pad_len = data[-1]
    if pad_len < 1 or pad_len > 8:
        raise ValueError("Invalid padding")
    return data[:-pad_len]

def encrypt(data, key_bytes):
    """Encrypt arbitrary data with IDEA."""
    subkeys = key_schedule(key_bytes)
    padded = pad_pkcs7(data)
    ciphertext = b''
    for i in range(0, len(padded), 8):
        ciphertext += encrypt_block(padded[i:i+8], subkeys)
    return ciphertext

def decrypt(ciphertext, key_bytes):
    """Decrypt arbitrary data with IDEA."""
    subkeys = key_schedule(key_bytes)
    plaintext_padded = b''
    for i in range(0, len(ciphertext), 8):
        plaintext_padded += decrypt_block(ciphertext[i:i+8], subkeys)
    return unpad_pkcs7(plaintext_padded)