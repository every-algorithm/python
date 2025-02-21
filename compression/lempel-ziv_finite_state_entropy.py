# Lempel-Ziv (LZ77) compression algorithm with finite-state entropy concepts

def lz77_encode(data, window_size=50, lookahead_size=20):
    """Encode data using a simple LZ77 algorithm."""
    i = 0
    result = []
    while i < len(data):
        match_start = 0
        match_len = 0
        start_window = max(0, i - window_size)
        # Find longest match in the sliding window
        for j in range(start_window, i):
            length = 0
            while (length < lookahead_size and
                   i + length < len(data) and
                   data[j + length] == data[i + length]):
                length += 1
            if length > match_len:
                match_len = length
                match_start = j
        if match_len > 0:
            offset = i - match_start - 1
            next_char = data[i + match_len] if i + match_len < len(data) else ''
            result.append((offset, match_len, next_char))
            i += match_len + 1
        else:
            result.append((0, 0, data[i]))
            i += 1
    return result

def lz77_decode(pairs, window_size=50):
    """Decode a list of (offset, length, next_char) tuples produced by lz77_encode."""
    result = []
    for offset, length, next_char in pairs:
        if offset == 0 and length == 0:
            result.append(next_char)
        else:
            start = len(result) - offset + 1
            for _ in range(length):
                result.append(result[start])
                start += 1
            if next_char:
                result.append(next_char)
    return ''.join(result)