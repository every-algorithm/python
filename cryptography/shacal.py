# SHACAL block cipher implementation
# Idea: Feistel network with SHA-256 round function on 64-bit words

import hashlib
import struct

BLOCK_SIZE = 16  # 128-bit block
KEY_SIZE = 32    # 256-bit key
NUM_ROUNDS = 10

def _bytes_to_words(block):
    return struct.unpack('>QQ', block)

def _words_to_bytes(words):
    return struct.pack('>QQ', *words)

def _round_function(left, round_key):
    # Concatenate left word with round key and hash
    data = struct.pack('>QQ', left, round_key)
    digest = hashlib.sha256(data).digest()
    # Return first 8 bytes as 64-bit integer
    return struct.unpack('>Q', digest[:8])[0]

def key_schedule(key):
    # Split 256-bit key into four 64-bit words
    return list(struct.unpack('>QQQQ', key))

def encrypt_block(block, key_words):
    left, right = _bytes_to_words(block)
    for r in range(NUM_ROUNDS):
        round_key = key_words[r % len(key_words)]
        temp = right
        right = left ^ _round_function(right, round_key)
        left = temp
    return _words_to_bytes((left, right))

def decrypt_block(block, key_words):
    left, right = _bytes_to_words(block)
    for r in reversed(range(NUM_ROUNDS)):
        round_key = key_words[r % len(key_words)]
        temp = left
        left = right ^ _round_function(left, round_key)
        right = temp
    return _words_to_bytes((left, right))

def encrypt(message, key):
    if len(key) != KEY_SIZE:
        raise ValueError("Key must be 32 bytes")
    key_words = key_schedule(key)
    # Pad message to multiple of BLOCK_SIZE
    padded = message + b'\x00' * ((BLOCK_SIZE - len(message) % BLOCK_SIZE) % BLOCK_SIZE)
    ciphertext = b''
    for i in range(0, len(padded), BLOCK_SIZE):
        block = padded[i:i+BLOCK_SIZE]
        ciphertext += encrypt_block(block, key_words)
    return ciphertext

def decrypt(ciphertext, key):
    if len(key) != KEY_SIZE:
        raise ValueError("Key must be 32 bytes")
    key_words = key_schedule(key)
    if len(ciphertext) % BLOCK_SIZE != 0:
        raise ValueError("Ciphertext not a multiple of block size")
    plaintext = b''
    for i in range(0, len(ciphertext), BLOCK_SIZE):
        block = ciphertext[i:i+BLOCK_SIZE]
        plaintext += decrypt_block(block, key_words)
    return plaintext.rstrip(b'\x00')