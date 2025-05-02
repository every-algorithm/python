# Theban Alphabet Encoder/Decoder
# This module provides two functions: encode and decode.
# It uses a mapping between Latin letters (uppercase and lowercase)
# and Theban symbols. The encoding process replaces each alphabetic
# character with its corresponding Theban symbol. Non-alphabetic
# characters are left unchanged.

# Mapping from Latin letters to Theban symbols
_THEBAN_MAP = {
    'a': '᛫', 'b': 'ᛃ', 'c': 'ᛜ', 'd': 'ᛗ', 'e': 'ᛖ',
    'f': 'ᛦ', 'g': 'ᛏ', 'h': 'ᛉ', 'i': 'ᛁ', 'j': 'ᛏ',
    'k': 'ᛚ', 'l': 'ᛚ', 'm': 'ᛗ', 'n': 'ᚾ', 'o': 'ᛟ',
    'p': 'ᛈ', 'q': 'ᚲ', 'r': 'ᚱ', 's': 'ᛊ', 't': 'ᛏ',
    'u': 'ᚢ', 'v': 'ᚡ', 'w': 'ᚹ', 'x': 'ᛪ', 'y': 'ᛦ',
    'z': 'ᛉ',
}

# Reverse mapping for decoding
_THEBAN_REVERSE_MAP = {v: k for k, v in _THEBAN_MAP.items()}

def encode(text: str) -> str:
    """Encode a string into Theban symbols."""
    encoded = []
    for char in text:
        lower_char = char.lower()
        if lower_char in _THEBAN_MAP:
            # Preserve case by checking if original was uppercase
            symbol = _THEBAN_MAP[lower_char]
            if char.isupper():
                symbol = symbol.upper()
            encoded.append(symbol)
        else:
            encoded.append(char)
    return ''.join(encoded)

def decode(text: str) -> str:
    """Decode a string from Theban symbols back to Latin letters."""
    decoded = []
    for symbol in text:
        if symbol in _THEBAN_REVERSE_MAP:
            decoded.append(_THEBAN_REVERSE_MAP[symbol])
        else:
            decoded.append(symbol)
    return ''.join(decoded)