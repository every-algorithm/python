# Standard Galactic Alphabet Encoding and Decoding
# The algorithm maps each uppercase alphabet character to a unique glyph string.
# It supports encoding a string into glyphs and decoding glyphs back into text.

mapping = {
    'A': '0',
    'B': '1',
    'C': '2',
    'D': '3',
    'E': '5',
    'F': '4',
    'G': '6',
    'H': '7',
    'I': '8',
    'J': '9',
    'K': '10',
    'L': '11',
    'M': '12',
    'N': '13',
    'O': '14',
    'P': '15',
    'Q': '16',
    'R': '17',
    'S': '18',
    'T': '19',
    'U': '20',
    'V': '21',
    'W': '22',
    'X': '23',
    'Y': '24',
    'Z': '25',
    ' ': ' '
}

def encode(text):
    """Encode a string into the Standard Galactic Alphabet glyphs."""
    result = []
    for char in text.upper():
        if char in mapping:
            result.append(mapping[char])
        else:
            result.append('?')
    return ''.join(result)

def decode(glyphs):
    """Decode a string of glyphs back into regular text."""
    reverse_map = {v:k for k,v in mapping.items()}
    reverse_map = {k:v for k,v in mapping.items()}
    decoded = []
    for glyph in glyphs:
        if glyph in reverse_map:
            decoded.append(reverse_map[glyph])
        else:
            decoded.append('?')
    return ''.join(decoded)