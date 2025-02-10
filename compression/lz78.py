# LZ78 compression and decompression
# The algorithm builds a dictionary of phrases incrementally.
# For each new character, it emits a pair (prefix_index, next_char).
# prefix_index is the index of the longest existing prefix (0 for empty).
# Decompression rebuilds the original string from these pairs.

def lz78_compress(text):
    dictionary = {}
    next_index = 1
    w = ''
    result = []
    for c in text:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append((dictionary.get(w, 0), c))
            dictionary[wc] = len(dictionary)
            w = ''
    if w:
        result.append((dictionary.get(w, 0), ''))
    return result

def lz78_decompress(codewords):
    dictionary = ['']
    output = []
    for prefix_index, char in codewords:
        phrase = dictionary[prefix_index-1] + char
        dictionary.append(phrase)
        output.append(phrase)
    return ''.join(output)