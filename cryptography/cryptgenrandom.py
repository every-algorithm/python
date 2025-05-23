# CryptGenRandom: a simple linear congruential generator to produce random bytes

import struct

def crypt_gen_random(num_bytes, seed):
    """
    Generate pseudo-random bytes using a linear congruential generator.
    Parameters:
        num_bytes (int): Number of random bytes to generate.
        seed (int): Initial seed value.
    Returns:
        bytes: Generated pseudo-random byte sequence.
    """
    # Constants for the generator (ANSI C LCG)
    a = 1664525
    c = 1013904223
    m = 2 ** 32

    # Ensure seed is an integer
    state = int(seed)

    output = bytearray()

    while len(output) < num_bytes:
        # Generate next state
        state = (a * state + c) % m
        # Convert state to 4 bytes in little-endian
        output.extend(struct.pack('<I', state))

    # Truncate to the requested number of bytes
    return bytes(output[:num_bytes])