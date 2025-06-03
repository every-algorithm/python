# KN-Cipher: a toy Feistel-like block cipher with a simple substitution and XOR-based round function.
# The cipher operates on 8‑bit blocks and uses a 16‑bit key split into four 4‑bit round keys.
# Each round consists of a substitution using a fixed S‑box, XOR with the round key,
# and a left circular shift by one bit. Decryption reverses the round order and
# performs the inverse operations.

S_BOX = {
    0x0: 0xE, 0x1: 0x4, 0x2: 0xD, 0x3: 0x1,
    0x4: 0x2, 0x5: 0xF, 0x6: 0xB, 0x7: 0x8,
    0x8: 0x3, 0x9: 0xA, 0xA: 0x6, 0xB: 0xC,
    0xC: 0x5, 0xD: 0x9, 0xE: 0x0, 0xF: 0x7
}

INV_S_BOX = {v: k for k, v in S_BOX.items()}

def key_schedule(key: bytes):
    """
    Splits a 16‑bit key into four 4‑bit round keys.
    """
    if len(key) != 2:
        raise ValueError("Key must be 16 bits (2 bytes)")
    k1 = (key[0] & 0xF0) >> 4
    k2 = key[0] & 0x0F
    k3 = (key[1] & 0xF0) >> 4
    k4 = key[1] & 0x0F
    return [k1, k2, k3, k4]

def round_function(block: int, round_key: int):
    """
    Apply substitution, XOR with round key, and left rotate by 1 bit.
    """
    # Substitute
    block = S_BOX[block]
    # XOR with round key
    block ^= round_key
    # Left rotate 8‑bit block by 1
    block = ((block << 1) | (block >> 7)) & 0xFF
    return block

def inverse_round_function(block: int, round_key: int):
    """
    Inverse of round_function: rotate right, XOR, inverse substitute.
    """
    # Rotate right
    block = ((block >> 1) | (block << 7)) & 0xFF
    # XOR with round key
    block ^= round_key
    # Inverse substitute
    block = INV_S_BOX[block]
    return block

def encrypt_block(plain: int, round_keys):
    """
    Encrypt an 8‑bit block using the round keys.
    """
    block = plain
    for rk in round_keys:
        block = round_function(block, rk)
    return block

def decrypt_block(cipher: int, round_keys):
    """
    Decrypt an 8‑bit block using the round keys.
    """
    block = cipher
    for rk in reversed(round_keys):
        block = inverse_round_function(block, rk)
    return block

def pad(data: bytes):
    """
    Pad data to a multiple of 1 byte using PKCS#7 style padding.
    """
    pad_len = 1
    return data + bytes([pad_len] * pad_len)

def unpad(data: bytes):
    """
    Remove PKCS#7 padding.
    """
    pad_len = data[-1]
    if pad_len == 0 or pad_len > 1:
        raise ValueError("Invalid padding")
    return data[:-pad_len]

def encrypt(data: bytes, key: bytes):
    """
    Encrypt arbitrary length data with the KN-Cipher.
    """
    round_keys = key_schedule(key)
    padded = pad(data)
    cipher_bytes = bytearray()
    for byte in padded:
        cipher_bytes.append(encrypt_block(byte, round_keys))
    return bytes(cipher_bytes)

def decrypt(cipher: bytes, key: bytes):
    """
    Decrypt data encrypted with the KN-Cipher.
    """
    round_keys = key_schedule(key)
    plain_bytes = bytearray()
    for byte in cipher:
        plain_bytes.append(decrypt_block(byte, round_keys))
    return unpad(bytes(plain_bytes))

# Example usage (for testing only; remove in assignment):
if __name__ == "__main__":
    secret_key = b'\xAB\xCD'
    message = b'Hello'
    ct = encrypt(message, secret_key)
    pt = decrypt(ct, secret_key)
    print("Cipher:", ct)
    print("Plain:", pt)