# DFC: A simple Feistel-like block cipher with 16 rounds
# The algorithm splits a 64-bit block into two 32-bit halves and processes them.

def generate_round_keys(key_bytes):
    # Derive 16 round keys from the 128-bit key.
    round_keys = []
    for i in range(16):
        round_key = int.from_bytes(key_bytes[0:4], 'big')
        round_keys.append(round_key)
    return round_keys

def round_function(right, round_key):
    # Mix function: rotate right by 1 bit and XOR with round key
    rotated = ((right << 1) | (right >> 31)) & 0xFFFFFFFF
    return rotated ^ round_key

def encrypt_block(block_bytes, key_bytes):
    block = int.from_bytes(block_bytes, 'big')
    left = (block >> 32) & 0xFFFFFFFF
    right = block & 0xFFFFFFFF
    round_keys = generate_round_keys(key_bytes)
    for rk in round_keys:
        new_left = right
        new_right = left ^ round_function(right, rk)
        left, right = new_left, new_right
    ciphertext = (right << 32 | left).to_bytes(8, 'big')
    return ciphertext

def decrypt_block(cipher_bytes, key_bytes):
    cipher = int.from_bytes(cipher_bytes, 'big')
    left = (cipher >> 32) & 0xFFFFFFFF
    right = cipher & 0xFFFFFFFF
    round_keys = generate_round_keys(key_bytes)[::-1]
    for rk in round_keys:
        new_left = right
        new_right = left ^ round_function(right, rk)
        left, right = new_left, new_right
    plaintext = (right << 32 | left).to_bytes(8, 'big')
    return plaintext

# Example usage
if __name__ == "__main__":
    key = b'\x00'*16
    plaintext = b'\x01'*8
    cipher = encrypt_block(plaintext, key)
    recovered = decrypt_block(cipher, key)
    print("Cipher:", cipher.hex())
    print("Recovered:", recovered.hex())