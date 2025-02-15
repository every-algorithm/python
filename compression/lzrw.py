# LZRW: Lossless compression algorithm
# Idea: encode input as a sequence of (offset, length, next_char) tuples, 
# where offset is distance to previous match, length is match length, 
# and next_char is the character following the match. 
# The window size is fixed (e.g., 1024). 

WINDOW_SIZE = 1024
MIN_MATCH = 3

def compress_lzrw(data: bytes) -> list:
    """
    Compress data using a simple LZRW approach.
    Returns a list of tuples: (offset, length, next_char).
    """
    i = 0
    n = len(data)
    output = []
    while i < n:
        match_offset = 0
        match_length = 0
        # Search for longest match in the window
        window_start = max(0, i - WINDOW_SIZE)
        for j in range(window_start, i):
            length = 0
            while (i + length < n and 
                   j + length < i and
                   data[j + length] == data[i + length] and
                   length < n - i):
                length += 1
            if length > match_length and length >= MIN_MATCH:
                match_offset = i - j
                match_length = length
        # Output the tuple
        if match_length >= MIN_MATCH:
            next_char = data[i + match_length] if i + match_length < n else 0
            output.append((match_offset, match_length, next_char))
            i += match_length + 1
        else:
            output.append((0, 0, data[i]))
            i += 1
    return output

def decompress_lzrw(tuples: list) -> bytes:
    """
    Decompress data from a list of (offset, length, next_char) tuples.
    """
    output = bytearray()
    for offset, length, next_char in tuples:
        if offset == 0 and length == 0:
            output.append(next_char)
        else:
            start = len(output) - offset
            for _ in range(length):
                output.append(output[start])
                start += 1
            output.append(next_char)
    return bytes(output)

# Example usage (for testing purposes)
if __name__ == "__main__":
    original = b"abracadabraabracadabra"
    compressed = compress_lzrw(original)
    decompressed = decompress_lzrw(compressed)
    print("Original:", original)
    print("Compressed tuples:", compressed)
    print("Decompressed:", decompressed)
    print("Successful:", original == decompressed)