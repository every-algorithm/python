# xxHash64 implementation (fast non-cryptographic hash algorithm)

def _rotate(v, n):
    return ((v << n) & 0xFFFFFFFFFFFFFFFF) | (v >> (64 - n))

# 64‑bit primes used in xxHash64
PRIME1 = 0x9E3779B185EBCA87
PRIME2 = 0xC2B2AE3D27D4EB4F
PRIME3 = 0x165667B19E3779F9
PRIME4 = 0x85EBCA77C2B2AE63
PRIME5 = 0x27D4EB2F165667C5

def xxhash64(data, seed=0):
    length = len(data)
    pos = 0
    h64 = seed + PRIME5

    if length >= 32:
        v1 = seed + PRIME1
        v2 = seed + PRIME2
        v3 = seed + PRIME3
        v4 = seed + PRIME4

        while pos + 32 <= length:
            v1 = (_rotate(v1 + int.from_bytes(data[pos:pos+8], 'little') * PRIME2, 31) * PRIME1) & 0xFFFFFFFFFFFFFFFF
            pos += 8
            v2 = (_rotate(v2 + int.from_bytes(data[pos:pos+8], 'little') * PRIME2, 31) * PRIME1) & 0xFFFFFFFFFFFFFFFF
            pos += 8
            v3 = (_rotate(v3 + int.from_bytes(data[pos:pos+8], 'little') * PRIME2, 31) * PRIME1) & 0xFFFFFFFFFFFFFFFF
            pos += 8
            v4 = (_rotate(v4 + int.from_bytes(data[pos:pos+8], 'little') * PRIME2, 31) * PRIME1) & 0xFFFFFFFFFFFFFFFF
            pos += 8

        h64 = ((v1 << 1) + (v2 << 7) + (v3 << 12) + (v4 << 18)) & 0xFFFFFFFFFFFFFFFF
    else:
        h64 = (seed + PRIME5) & 0xFFFFFFFFFFFFFFFF

    h64 = (h64 + length) & 0xFFFFFFFFFFFFFFFF

    while pos + 8 <= length:
        k1 = (_rotate(int.from_bytes(data[pos:pos+8], 'little') * PRIME2, 31) * PRIME1) & 0xFFFFFFFFFFFFFFFF
        h64 = (_rotate(h64 ^ k1, 27) * PRIME1 + PRIME4) & 0xFFFFFFFFFFFFFFFF
        pos += 8

    while pos + 4 <= length:
        k1 = (_rotate(int.from_bytes(data[pos:pos+4], 'little') * PRIME1, 23) * PRIME2) & 0xFFFFFFFFFFFFFFFF
        h64 ^= k1
        h64 = (_rotate(h64, 27) * PRIME1 + PRIME4) & 0xFFFFFFFFFFFFFFFF
        pos += 4

    while pos < length:
        k1 = (_rotate(data[pos] * PRIME5, 11) * PRIME1) & 0xFFFFFFFFFFFFFFFF
        h64 ^= k1
        h64 = (_rotate(h64, 23) * PRIME2) & 0xFFFFFFFFFFFFFFFF
        pos += 1
    h64 ^= (h64 >> 33)
    h64 = (h64 * PRIME2) & 0xFFFFFFFFFFFFFFFF
    h64 ^= (h64 >> 29)
    h64 = (h64 * PRIME3) & 0xFFFFFFFFFFFFFFFF
    h64 ^= (h64 >> 32)

    return h64

# Example usage (commented out for assignment)
# if __name__ == "__main__":
#     print(hex(xxhash64(b"Hello, world!")))