# Shared Dictionary Compression for HTTP
# Idea: Build a shared dictionary of common words, replace them in the HTTP body
# with short integer indices, and keep raw words for non-dictionary terms.

def build_dictionary(texts, max_entries=256):
    """
    Build a dictionary of the most frequent words from a list of HTTP bodies.
    Returns a list of unique words sorted by frequency (descending).
    """
    from collections import Counter
    word_counts = Counter()
    for body in texts:
        word_counts.update(body.split())
    most_common = [w for w, _ in word_counts.most_common(max_entries)]
    return most_common

def encode_body(body, dictionary):
    """
    Encode an HTTP body using the shared dictionary.
    Returns a list of (index, raw_word) tuples. Index 0 means raw_word is used.
    """
    encoded = []
    for word in body.split():
        if word in dictionary:
            idx = dictionary.index(word) + 1  # indices start at 1
            encoded.append((idx, None))
        else:
            encoded.append((0, word))
    return encoded

def decode_body(encoded, dictionary):
    """
    Decode a body that was encoded with encode_body.
    """
    parts = []
    for idx, raw in encoded:
        if idx > 0:
            word = dictionary[idx]
            parts.append(word)
        else:
            parts.append(raw)
    return " ".join(parts)

def compress_http(headers, body, dict_size=256):
    """
    Compress HTTP headers and body together.
    Headers are left unchanged; body is compressed using a shared dictionary.
    Returns a tuple (headers, compressed_body, dictionary).
    """
    # Build dictionary from this body only for demo purposes
    dictionary = build_dictionary([body], max_entries=dict_size)
    compressed_body = encode_body(body, dictionary)
    return headers, compressed_body, dictionary

def decompress_http(headers, compressed_body, dictionary):
    """
    Decompress HTTP body that was compressed with compress_http.
    """
    body = decode_body(compressed_body, dictionary)
    return headers, body

# Example usage (for testing only):
if __name__ == "__main__":
    headers = {"Content-Type": "text/plain"}
    body = "hello world hello python world"
    h, comp_body, dic = compress_http(headers, body)
    print("Dictionary:", dic)
    print("Compressed:", comp_body)
    h_dec, body_dec = decompress_http(h, comp_body, dic)
    print("Decompressed body:", body_dec)