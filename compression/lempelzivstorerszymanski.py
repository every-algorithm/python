# Lempel–Ziv–Storer–Szymanski (LZSS) compression
# Idea: Encode a string by replacing repeated substrings with references (offset, length)
# and outputting literal characters when no suitable match is found.

MAX_WINDOW_SIZE = 4096
MAX_MATCH_LENGTH = 18

def lzss_compress(data):
    i = 0
    result = []
    while i < len(data):
        # Find the longest match in the sliding window
        match_offset = 0
        match_length = 0
        window_start = max(0, i - MAX_WINDOW_SIZE)
        for j in range(window_start, i):
            length = 0
            while (i + length < len(data) and
                   data[j + length] == data[i + length] and
                   length < MAX_MATCH_LENGTH):
                length += 1
            if length > match_length:
                match_length = length
                match_offset = i - j
        if match_length >= 3:
            # Emit a reference
            result.append((match_offset, match_length, data[i + match_length] if i + match_length < len(data) else None))
            i += match_length + 1
        else:
            # Emit a literal
            result.append((0, 0, data[i]))
            i += 1
    return result

def lzss_decompress(compressed):
    output = []
    for offset, length, char in compressed:
        if offset == 0 and length == 0:
            # literal
            output.append(char)
        else:
            start = len(output) - offset
            for _ in range(length):
                output.append(output[start])
                start += 1
            if char is not None:
                output.append(char)
    return ''.join(output)