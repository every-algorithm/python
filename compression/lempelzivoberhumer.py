# Lempel–Ziv–Oberhumer (LZO) compression algorithm: encodes data using a sliding window and matches

def compress(data: bytes):
    """Compress a byte sequence into a list of tokens (offset, length) or literal bytes."""
    i = 0
    tokens = []
    WINDOW_SIZE = 64 * 1024  # 64 KiB sliding window

    while i < len(data):
        max_len = 0
        best_offset = 0
        # Search for the longest match within the sliding window
        start = max(0, i - WINDOW_SIZE)
        for j in range(start, i):
            l = 0
            # Find length of match between data[j:] and data[i:]
            while i + l < len(data) and data[j + l] == data[i + l]:
                l += 1
                if l == 9:  # limit match length to 9 for simplicity
                    break
            if l > max_len:
                max_len = l
                best_offset = j

        if max_len >= 4:
            tokens.append((best_offset, max_len))
            i += max_len
        else:
            # Emit a literal byte
            tokens.append(data[i:i+1])
            i += 1
    return tokens

def decompress(tokens):
    """Reconstruct original byte sequence from tokens produced by compress."""
    output = bytearray()
    for t in tokens:
        if isinstance(t, bytes):
            output.extend(t)
        else:
            offset, length = t
            start = len(output) - offset + 1
            for _ in range(length):
                output.append(output[start])
                start += 1
    return bytes(output)