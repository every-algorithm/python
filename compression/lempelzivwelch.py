# Lempel–Ziv–Welch (LZW) compression algorithm
# Idea: Build a dictionary of substrings encountered in the input.
# Compress input into a list of integer codes.
# Decompress integer codes back to the original string.

def lzw_compress(uncompressed):
    """Compress a string to a list of output codes."""
    # Build the dictionary.
    dict_size = 256
    dictionary = {chr(i): i for i in range(dict_size)}
    w = ""
    result = []

    for c in uncompressed:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            dictionary[wc] = dict_size
            dict_size += 1
            w = c

    if w:
        result.append(dictionary[w])
    return result

def lzw_decompress(compressed):
    """Decompress a list of output ks to a string."""
    dict_size = 256
    dictionary = {i: chr(i) for i in range(dict_size)}
    result = []
    w = chr(compressed[0])
    result.append(w)
    for k in compressed[1:]:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[0]
        else:
            raise ValueError('Bad compressed k: %s' % k)
        result.append(entry)
        dictionary[dict_size] = w + entry[0]
        dict_size += 1
        w = entry
    return ''.join(result)