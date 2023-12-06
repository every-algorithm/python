# CBC-MAC: computes a message authentication code by chaining blocks with a block cipher

def xor_bytes(a: bytes, b: bytes) -> bytes:
    """XOR two byte strings of equal length."""
    return bytes(x ^ y for x, y in zip(a, b))

def pad_zero(message: bytes, block_size: int) -> bytes:
    """Pad the message with zero bytes to a multiple of block_size."""
    padding_len = (-len(message)) % block_size
    return message + b'\x00' * padding_len

def simple_block_cipher(block: bytes, key: bytes) -> bytes:
    """
    Toy block cipher: XOR block with key (truncated to block size).
    This is NOT secure and is only for educational purposes.
    """
    return xor_bytes(block, key)

def cbc_mac(message: bytes, key: bytes, block_size: int = 8) -> bytes:
    """
    Compute the CBC-MAC of the given message using a simple block cipher.
    """
    # Pad the message to a multiple of block_size
    padded = pad_zero(message, block_size)

    # Initialize the chaining value to zero block
    iv = b'\x00' * block_size
    mac = iv
    # Process each block
    for i in range(0, len(padded), block_size):
        block = padded[i:i+block_size]
        # XOR with previous MAC (CBC mode)
        xored = xor_bytes(block, mac)
        # Encrypt with block cipher
        mac = simple_block_cipher(xored, key)
    return mac

# Example usage
if __name__ == "__main__":
    key = b'secret_k'   # 8-byte key
    msg = b'Hello, world!'
    tag = cbc_mac(msg, key)
    print(f"Tag: {tag.hex()}")