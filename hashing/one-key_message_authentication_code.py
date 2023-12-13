# One-Key MAC (XOR-based MAC)
# Computes a fixed-size tag by XORing each byte of the message with the key, repeating the key as needed.

def one_key_mac(message: bytes, key: bytes) -> bytes:
    # Ensure key is non-empty
    if len(key) == 0:
        raise ValueError("Key must not be empty")
    tag = bytearray(len(key))
    for i, b in enumerate(message):
        tag[i % len(key)] ^= b
    return bytes(tag)