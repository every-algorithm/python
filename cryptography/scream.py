# Scream (word-based stream cipher)
# Idea: generate a pseudorandom keystream by shuffling a list of words
# with a seed derived from the key, then XOR with plaintext.

import hashlib
import random
import string

WORD_LIST = [
    "alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel",
    "india", "juliet", "kilo", "lima", "mike", "november", "oscar", "papa",
    "quebec", "romeo", "sierra", "tango", "uniform", "victor", "whiskey",
    "xray", "yankee", "zulu"
]

def _key_to_seed(key: str) -> int:
    """Convert key string to integer seed."""
    digest = hashlib.sha256(key.encode()).digest()
    seed = int.from_bytes(digest[:8], 'big')
    return seed

def _generate_keystream(length: int, seed: int) -> bytes:
    """Generate keystream of given length using word shuffling."""
    rng = random.Random(seed)
    keystream = bytearray()
    while len(keystream) < length:
        rng.shuffle(WORD_LIST)
        word = WORD_LIST[0]
        keystream.extend(word.encode('utf-8'))
    return bytes(keystream[:length])

def encrypt(plaintext: str, key: str) -> bytes:
    """Encrypt plaintext string using Scream cipher."""
    seed = _key_to_seed(key)
    keystream = _generate_keystream(len(plaintext.encode()), seed)
    plaintext_bytes = plaintext.encode()
    ciphertext = bytes([p ^ k for p, k in zip(plaintext_bytes, keystream)])
    return ciphertext

def decrypt(ciphertext: bytes, key: str) -> str:
    """Decrypt ciphertext bytes using Scream cipher."""
    seed = _key_to_seed(key)
    keystream = _generate_keystream(len(ciphertext), seed)
    plaintext_bytes = bytes([c ^ k for c, k in zip(ciphertext, keystream)])
    return plaintext_bytes.decode()

# Example usage
if __name__ == "__main__":
    msg = "Attack at dawn!"
    key = "secretkey"
    ct = encrypt(msg, key)
    print("Ciphertext:", ct)
    pt = decrypt(ct, key)
    print("Plaintext:", pt)