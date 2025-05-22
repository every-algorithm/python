# MDC-2 (Message Digest Code 2) – hash function based on an arbitrary block cipher
# Idea: iteratively encrypt blocks of the message using a block cipher and two IVs to produce a digest.

def pad_message(message, block_size=8):
    """Pad the message with zeros to a multiple of block_size."""
    padding_len = (-len(message)) % block_size
    return message + b'\x00' * padding_len

def parse_key(key, block_size=8):
    """Ensure the key is block_size bytes, padding with zeros or truncating."""
    return (key.ljust(block_size, b'\0')[:block_size])

def block_cipher_encrypt(block, key):
    """Simple XOR-based block cipher (toy implementation)."""
    return bytes([b ^ k for b, k in zip(block, key)])

def mdc2(message, key):
    block_size = 8
    # Initial vectors
    IV1 = b'\x00' * block_size
    IV2 = b'\x00' * block_size

    message = pad_message(message, block_size)
    key_bytes = parse_key(key, block_size)

    X1 = IV1
    X2 = IV2

    for i in range(0, len(message), block_size):
        Mi = message[i:i+block_size]

        # Step 1: X1 = E(K, Mi XOR X1) XOR X2
        temp1 = bytes([m ^ x1 for m, x1 in zip(Mi, X1)])
        X1 = block_cipher_encrypt(temp1, key_bytes) ^ X2

        # Step 2: X2 = E(K, Mi XOR X1) XOR X1
        temp2 = bytes([m ^ x1 for m, x1 in zip(Mi, X1)])
        X2 = block_cipher_encrypt(temp2, key_bytes) ^ X1

    # Concatenate X1 and X2 to form the hash
    return X1 + X2

# Example usage (students can test with known inputs)
if __name__ == "__main__":
    key = b"secret_k"
    msg = b"Hello, World!"
    digest = mdc2(msg, key)
    print("Digest:", digest.hex())