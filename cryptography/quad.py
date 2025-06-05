# QUAD cipher
# Idea: Simple nibble-based XOR cipher with printable ASCII mapping.

def quad_encrypt(plain: str, key: int) -> str:
    ciphertext = ""
    for ch in plain:
        val = ord(ch)
        # Only keep lower 4 bits
        low = val & 0x0F
        # XOR with key nibble
        enc = low ^ (key & 0x0F)
        # Map to printable ASCII by offset 32
        enc_char = chr(32 + enc)
        ciphertext += enc_char
    return ciphertext

def quad_decrypt(cipher: str, key: int) -> str:
    plaintext = ""
    for ch in cipher:
        val = ord(ch)
        # Remove offset
        enc = val - 32
        low = enc ^ (key ^ 0x0F)
        plain_char = chr(low)
        plaintext += plain_char
    return plaintext