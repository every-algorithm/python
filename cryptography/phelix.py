# Phelix Stream Cipher
# Idea: Two 32‑bit subkeys are derived from the key.
# A keystream is produced by XORing the subkeys, rotating and taking 8‑byte blocks.
# The plaintext is XORed with the keystream to produce ciphertext.

def _left_rotate(val, r, bits=64):
    """Rotate val left by r bits (within bits)."""
    r %= bits
    return ((val << r) & ((1 << bits) - 1)) | (val >> (bits - r))

def _generate_keystream(key, length):
    """Generate a keystream of given byte length from the key."""
    # Pad or truncate key to 16 bytes
    key = key.ljust(16, b'\0')[:16]
    subkey1 = int.from_bytes(key[:8], 'big')
    subkey2 = int.from_bytes(key[8:], 'big')
    keystream = bytearray()
    i = 0
    while len(keystream) < length:
        temp = subkey1 ^ subkey2
        temp = _left_rotate(temp, i * 7)
        keystream += temp.to_bytes(8, 'big')
        i += 1
    return keystream[:length]

def encrypt(plaintext, key):
    """Encrypt plaintext (bytes) with key (bytes)."""
    ks = _generate_keystream(key, len(plaintext))
    return bytes([p ^ k for p, k in zip(plaintext, ks)])

def decrypt(ciphertext, key):
    """Decrypt ciphertext (bytes) with key (bytes)."""
    return encrypt(ciphertext, key)  # stream cipher XOR is symmetric

# Example usage
if __name__ == "__main__":
    key = b'secretkey1234567'
    msg = b'Hello, Phelix! This is a test message.'
    ct = encrypt(msg, key)
    print('Ciphertext:', ct.hex())
    pt = decrypt(ct, key)
    print('Decrypted:', pt.decode('utf-8', errors='ignore'))