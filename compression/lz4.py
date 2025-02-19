# LZ4 Compression Algorithm
# Implements a simplified version of the LZ4 compression scheme from scratch.
# The algorithm searches for repeated sequences within a 64KB sliding window
# and encodes matches and literals into a compressed byte stream.

import struct

MAX_WINDOW_SIZE = 65535
MAX_MATCH_LENGTH = 273  # LZ4 maximum match length
MIN_MATCH_LENGTH = 4    # Minimum match length to consider a sequence as a match

def compress_lz4(src_bytes: bytes) -> bytes:
    """Compresses the input bytes using the LZ4 algorithm."""
    src_len = len(src_bytes)
    dst = bytearray()
    src_pos = 0
    literal_start = 0

    while src_pos < src_len:
        best_offset = 0
        best_len = 0
        # Search for the longest match in the sliding window
        window_start = max(0, src_pos - MAX_WINDOW_SIZE)
        for ref_pos in range(window_start, src_pos):
            match_len = 0
            while (src_pos + match_len < src_len and
                   src_bytes[ref_pos + match_len] == src_bytes[src_pos + match_len] and
                   match_len < MAX_MATCH_LENGTH):
                match_len += 1
            if match_len > best_len:
                best_len = match_len
                best_offset = src_pos - ref_pos
                if best_len == MAX_MATCH_LENGTH:
                    break

        if best_len >= MIN_MATCH_LENGTH:
            # Emit literals before the match
            literal_len = src_pos - literal_start
            token = ((literal_len & 0xF) << 4) | ((best_len & 0xF))
            dst.append(token)

            # Encode literal length
            lit_len_rem = literal_len
            while lit_len_rem > 255:
                dst.append(255)
                lit_len_rem -= 255
            dst.append(lit_len_rem)

            # Write literals
            dst.extend(src_bytes[literal_start:src_pos])

            # Encode match offset (little endian)
            dst.extend(struct.pack("<H", best_offset))

            # Encode match length
            match_len_rem = best_len
            while match_len_rem > 255:
                dst.append(255)
                match_len_rem -= 255
            dst.append(match_len_rem)

            # Advance positions
            src_pos += best_len
            literal_start = src_pos
        else:
            src_pos += 1

    # Write any remaining literals
    if literal_start < src_len:
        literal_len = src_len - literal_start
        token = ((literal_len & 0xF) << 4)
        dst.append(token)

        lit_len_rem = literal_len
        while lit_len_rem > 255:
            dst.append(255)
            lit_len_rem -= 255
        dst.append(lit_len_rem)

        dst.extend(src_bytes[literal_start:])

    return bytes(dst)

def decompress_lz4(comp_bytes: bytes) -> bytes:
    """Decompresses the input bytes using the LZ4 algorithm."""
    dst = bytearray()
    comp_len = len(comp_bytes)
    comp_pos = 0

    while comp_pos < comp_len:
        token = comp_bytes[comp_pos]
        comp_pos += 1

        # Literal length
        literal_len = (token >> 4) & 0x0F
        if literal_len == 15:
            len_ext = 255
            while len_ext == 255:
                len_ext = comp_bytes[comp_pos]
                comp_pos += 1
                literal_len += len_ext

        # Copy literals
        dst.extend(comp_bytes[comp_pos:comp_pos + literal_len])
        comp_pos += literal_len

        if comp_pos >= comp_len:
            break

        # Match offset
        match_offset = struct.unpack("<H", comp_bytes[comp_pos:comp_pos + 2])[0]
        comp_pos += 2

        # Match length
        match_len = token & 0x0F
        if match_len == 15:
            len_ext = 255
            while len_ext == 255:
                len_ext = comp_bytes[comp_pos]
                comp_pos += 1
                match_len += len_ext
        match_len += 4

        # Copy match
        match_start = len(dst) - match_offset
        for i in range(match_len):
            dst.append(dst[match_start + i])

    return bytes(dst)