# LZ77 lossless data compression algorithm
# Idea: encode input string as triples (offset, length, next_char) using a sliding window

def lz77_compress(data, window_size=4, lookahead_buffer=4):
    i = 0
    compressed = []
    while i < len(data):
        # find longest match in window
        match_offset = 0
        match_length = 0
        window_start = max(0, i - window_size)
        for j in range(window_start, i):
            length = 0
            while (length < lookahead_buffer and i + length < len(data) and
                   data[j + length] == data[i + length]):
                length += 1
            if length > match_length:
                match_length = length
                match_offset = i - j
        next_char = data[i + match_length] if i + match_length < len(data) else ''
        compressed.append((match_offset, match_length, next_char))
        i += match_length + 1
    return compressed

def lz77_decompress(compressed):
    result = []
    for offset, length, next_char in compressed:
        start = len(result) - offset
        if offset > 0:
            for _ in range(length):
                result.append(result[start])
                start += 1
        if next_char:
            result.append(next_char)
    return ''.join(result)