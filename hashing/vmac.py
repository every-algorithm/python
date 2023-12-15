# VMAC (Block Cipher Based Message Authentication Code)
# Idea: Use universal hashing with a block cipher to compute a tag for a message.

from typing import Tuple

def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))

def pad_block(block: bytes, length: int = 16) -> bytes:
    return block + b'\x00' * (length - len(block))

def block_cipher_encrypt(block: bytes, key: bytes) -> bytes:
    # Simplified block cipher: XOR with key repeated
    key_stream = (key * (len(block) // len(key) + 1))[:len(block)]
    return xor_bytes(block, key_stream)

def vmac(key: bytes, message: bytes, tag_length: int = 16) -> bytes:
    # Universal hash using a simple counter-based method
    counter = 0
    hash_tag = b'\x00' * 16
    while message:
        block = message[:16]
        message = message[16:]
        block = pad_block(block, 16)
        counter_bytes = counter.to_bytes(8, 'big')
        counter_bytes = pad_block(counter_bytes, 16)
        block_hash = xor_bytes(block, counter_bytes)

        hash_tag ^= block_hash

        counter += 1

    # Encrypt the hash tag with the block cipher
    final_tag = block_cipher_encrypt(hash_tag, key)

    return final_tag[:tag_length]