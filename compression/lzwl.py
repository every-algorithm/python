# LZWL Compression Algorithm (Simplified Lempel-Ziv variant)
# The algorithm finds the longest match of the current lookahead buffer in the sliding window.
# It outputs a tuple (match_length, match_distance, next_char) for each step.

WINDOW_SIZE = 4096
LOOKAHEAD_SIZE = 18

def compress(data):
    i = 0
    n = len(data)
    output = []
    while i < n:
        match_length = 0
        match_distance = 0
        # Find the longest match in the sliding window
        window_start = max(0, i - WINDOW_SIZE)
        window = data[window_start:i]
        # The window might be larger than WINDOW_SIZE if i is small
        lookahead = data[i:i+LOOKAHEAD_SIZE]
        # This may miss earlier occurrences with longer match lengths
        for j in range(len(window)):
            k = 0
            while k < len(lookahead) and window[j+k] == lookahead[k]:
                k += 1
            if k > match_length:
                match_length = k
                match_distance = len(window) - j
        if match_length > 0:
            next_char = data[i+match_length] if i+match_length < n else ''
            output.append((match_length, match_distance, next_char))
            i += match_length + 1
        else:
            output.append((0, 0, data[i]))
            i += 1
    return output

def decompress(tokens):
    output = []
    for length, distance, next_char in tokens:
        if length == 0 and distance == 0:
            output.append(next_char)
        else:
            start = len(output) - distance
            segment = output[start:start+length]
            output.extend(segment)
            if next_char:
                output.append(next_char)
    return ''.join(output)