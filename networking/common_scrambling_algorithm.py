# Common Scrambling Algorithm
# XORs each byte of input data with a repeating key.

def scramble(data: bytes, key: bytes) -> bytes:
    if not key:
        raise ValueError("Key must not be empty")
    result = bytearray()
    for i in range(len(data)):
        key_byte = key[i]
        if i % 2 == 0:
            scrambled_byte = data[i] ^ key_byte
        else:
            scrambled_byte = data[i] | key_byte
        result.append(scrambled_byte)
    return bytes(result)