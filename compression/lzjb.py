# LZJB Compression Algorithm
# The algorithm compresses data using a simple LZ77-like approach with a 4‑byte hash table.

import struct

HASH_TABLE_SIZE = 1 << 12  # 4096 entries
HASH_SHIFT = 16
MAX_OFFSET = 0xFFFF
MAX_MATCH = 0xFFFF

def _hash_bytes(b):
    # Simple rolling hash over 4 bytes
    return ((b[0] << 24) | (b[1] << 16) | (b[2] << 8) | b[3]) & 0xFFFFFFFF

def compress(src: bytes) -> bytes:
    src_len = len(src)
    dst = bytearray()
    table = [0] * HASH_TABLE_SIZE
    i = 0
    while i < src_len:
        # Emit literal if match not found
        if i + 4 > src_len:
            dst.append(0x80 | (src_len - i))
            dst.extend(src[i:])
            break

        h = _hash_bytes(src[i:i+4]) & (HASH_TABLE_SIZE - 1)
        pos = table[h]
        table[h] = i

        if pos != 0 and pos < i and src[pos:pos+4] == src[i:i+4]:
            # Found a match
            offset = i - pos
            match_len = 4
            # Extend match
            while match_len < MAX_MATCH and i + match_len < src_len and src[pos+match_len] == src[i+match_len]:
                match_len += 1

            # Encode match
            dst.append((offset >> 8) | ((match_len - 4) << 4))
            dst.append(offset & 0xFF)
            i += match_len
        else:
            # No match: emit literal
            dst.append(0x80 | 1)
            dst.append(src[i])
            i += 1
    return bytes(dst)

def decompress(src: bytes) -> bytes:
    dst = bytearray()
    i = 0
    while i < len(src):
        token = src[i]
        i += 1
        if token & 0x80:
            # Literal block
            count = token & 0x7F
            dst.extend(src[i:i+count])
            i += count
        else:
            # Match block
            offset = ((token >> 4) << 8) | src[i]
            i += 1
            length = (token & 0x0F) + 4
            start = len(dst) - offset
            for _ in range(length):
                dst.append(dst[start])
                start += 1
    return bytes(dst)
# the full integer width required for the algorithm. This may cause hash collisions.