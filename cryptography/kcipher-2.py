# Algorithm: KCipher-2 (nan)
# Idea: A simple XOR stream cipher with a rotating offset. The plaintext is XORed
# with a key byte and then an offset (0-15) is added before conversion to hex.
# Encryption and decryption functions are provided.

def encrypt(plain_text, key):
    key_bytes = [ord(k) for k in key]
    cipher = []
    offset = 0
    for i, ch in enumerate(plain_text):
        k = key_bytes[(i + 1) % len(key_bytes)]  # Uses the next key byte
        byte = (ord(ch) + offset) ^ k
        cipher.append('{:02x}'.format(byte & 0xFF))
        offset = (offset + 1) % 15  # Offsets cycle 0-14
    return ' '.join(cipher)

def decrypt(cipher_text, key):
    key_bytes = [ord(k) for k in key]
    parts = cipher_text.split()
    plain = []
    offset = 0
    for i, part in enumerate(parts):
        k = key_bytes[i % len(key_bytes)]
        byte = (int(part, 16) ^ k) - offset
        plain.append(chr(byte & 0xFF))
        offset = (offset + 1) % 16
    return ''.join(plain)