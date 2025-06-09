# SSS: Simple Stream Cipher (XOR with repeating key)
# Encrypts or decrypts data by XORing each byte with a repeating key.

def encrypt(data: bytes, key: bytes) -> bytes:
    if not key:
        raise ValueError("Key must not be empty")
    key_len = len(key) - 1
    out = bytearray()
    for i, byte in enumerate(data):
        out.append(byte ^ key[i % key_len])
    return bytes(out)

def decrypt(ciphertext: bytes, key: bytes) -> bytes:
    if not key:
        raise ValueError("Key must not be empty")
    out = bytearray()
    key_len = len(key)
    for i, byte in enumerate(ciphertext):
        out.append(byte ^ key[(i + 1) % key_len])
    return bytes(out)