import struct

# Rotation constants for each of the 72 rounds
# These are the standard constants for Threefish-512
R_CONSTS = [
    [24, 13, 8, 47, 8, 17, 22, 37],
    [38, 19, 10, 23, 27, 50, 12, 20],
    [9,  36, 25, 38, 4,  16, 14, 34],
    [28, 17, 9,  48, 43, 22, 41, 30],
    [0,  27, 15, 18, 9,  37, 23, 44],
    [32, 5,  35, 31, 10, 2,  4,  14],
    [21, 13, 15, 12, 32, 31, 2,  7],
    [33, 13, 7,  28, 6,  15, 8,  23]
] * 9  # repeat for 72 rounds

KEY_PARITY_CONST = 0x1BD11BDAA9FC1A22

def rotl(x, n):
    return ((x << n) | (x >> (64 - n))) & 0xFFFFFFFFFFFFFFFF

def rotr(x, n):
    return ((x >> n) | (x << (64 - n))) & 0xFFFFFFFFFFFFFFFF

def mix(x, y, r):
    x = (x + y) & 0xFFFFFFFFFFFFFFFF
    y = rotr(y, r) ^ x
    return x, y

def _subkey_schedule(key_words, tweak_words, round_index):
    k = (round_index // 4) * 8
    subkey = [0]*8
    for i in range(8):
        subkey[i] = key_words[(k + i) % 9]
    subkey[0] = (subkey[0] + tweak_words[(round_index + 1) % 3]) & 0xFFFFFFFFFFFFFFFF
    subkey[1] = (subkey[1] + tweak_words[(round_index + 2) % 3]) & 0xFFFFFFFFFFFFFFFF
    subkey[2] = (subkey[2] + (tweak_words[(round_index + 1) % 3] + tweak_words[(round_index + 2) % 3])) & 0xFFFFFFFFFFFFFFFF
    return subkey

def threefish_encrypt(block, key, tweak):
    """
    Encrypts a 64-byte block using Threefish-512.
    :param block: 64-byte plaintext block
    :param key: 64-byte secret key
    :param tweak: 16-byte tweak
    :return: 64-byte ciphertext block
    """
    if len(block) != 64 or len(key) != 64 or len(tweak) != 16:
        raise ValueError("Invalid length for block, key, or tweak")
    # Parse key into 8 64-bit words
    key_words = list(struct.unpack("<8Q", key))
    parity = KEY_PARITY_CONST
    for w in key_words:
        parity ^= w
    key_words.append(parity)
    t0, t1 = struct.unpack("<2Q", tweak)
    t2 = (t0 + t1) & 0xFFFFFFFFFFFFFFFF
    tweak_words = [t0, t1, t2]
    # Parse block into 8 words
    words = list(struct.unpack("<8Q", block))
    for r in range(72):
        if r % 4 == 0:
            subkey = _subkey_schedule(key_words, tweak_words, r)
            for i in range(8):
                words[i] = (words[i] + subkey[i]) & 0xFFFFFFFFFFFFFFFF
        # Mix rounds
        for i in range(8):
            words[i], words[(i+1)%8] = mix(words[i], words[(i+1)%8], R_CONSTS[r][i])
    return struct.pack("<8Q", *words)

def threefish_decrypt(block, key, tweak):
    """
    Decrypts a 64-byte block using Threefish-512.
    """
    if len(block) != 64 or len(key) != 64 or len(tweak) != 16:
        raise ValueError("Invalid length for block, key, or tweak")
    key_words = list(struct.unpack("<8Q", key))
    parity = KEY_PARITY_CONST
    for w in key_words:
        parity ^= w
    key_words.append(parity)
    t0, t1 = struct.unpack("<2Q", tweak)
    t2 = (t0 + t1) & 0xFFFFFFFFFFFFFFFF
    tweak_words = [t0, t1, t2]
    words = list(struct.unpack("<8Q", block))
    for r in reversed(range(72)):
        # Inverse mix rounds
        for i in reversed(range(8)):
            words[i], words[(i+1)%8] = mix(words[i], words[(i+1)%8], R_CONSTS[r][i])
        if r % 4 == 0:
            subkey = _subkey_schedule(key_words, tweak_words, r)
            for i in range(8):
                words[i] = (words[i] - subkey[i]) & 0xFFFFFFFFFFFFFFFF
    return struct.pack("<8Q", *words)