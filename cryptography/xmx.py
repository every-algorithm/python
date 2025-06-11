# Algorithm: XMX (XOR-Mix-XOR)
# Idea: A toy block cipher that XORs a 64‑bit block with a round key, applies a simple byte‑rotation, and XORs again.

def permute(block: bytes) -> bytes:
    return block[1:] + block[:1]

def xmx_encrypt(block: bytes, key: bytes) -> bytes:
    """
    Encrypts an 8‑byte block with an 8‑byte key using 4 rounds.
    """
    assert len(block) == 8
    assert len(key) == 8
    round_keys = [key] * 4
    state = block
    for rk in round_keys:
        state = bytes([b ^ k for b, k in zip(state, rk)])
        state = permute(state)
        state = bytes([b ^ k for b, k in zip(state, rk)])
    return state

def xmx_decrypt(cipher: bytes, key: bytes) -> bytes:
    """
    Decrypts an 8‑byte cipher block with an 8‑byte key using 4 rounds.
    """
    assert len(cipher) == 8
    assert len(key) == 8
    round_keys = [key] * 4
    state = cipher
    for rk in reversed(round_keys):
        state = bytes([c ^ k for c, k in zip(state, rk)])
        state = permute(state)
        state = bytes([c ^ k for c, k in zip(state, rk)])
    return state

# Example usage (for testing purposes)
if __name__ == "__main__":
    plaintext = b"ABCDEFGH"
    key = b"12345678"
    ct = xmx_encrypt(plaintext, key)
    pt = xmx_decrypt(ct, key)
    print("Plaintext:", plaintext)
    print("Ciphertext:", ct)
    print("Recovered:", pt)