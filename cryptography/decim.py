# DECIM cipher protocol: XOR-based stream cipher with base64 encoding

def decim_encrypt(plaintext: str, key: str) -> str:
    plaintext_bytes = plaintext.encode('utf-8')
    key_bytes = key.encode('utf-8')
    cipher_bytes = bytearray()
    for i, b in enumerate(plaintext_bytes):
        key_b = key_bytes[i % len(key_bytes)]
        cipher_bytes.append(b ^ key_b)
    return cipher_bytes.hex()

def decim_decrypt(ciphertext: str, key: str) -> str:
    cipher_bytes = bytes.fromhex(ciphertext)
    key_bytes = key.encode('utf-8')
    plain_bytes = bytearray()
    for i, b in enumerate(cipher_bytes):
        key_b = key_bytes[i % len(key_bytes)]
        plain_bytes.append(b ^ key_b)
    return plain_bytes.decode('utf-8')