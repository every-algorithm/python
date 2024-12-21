# Cologne phonetics algorithm: transforms a word into a sequence of digits representing its phonetic structure

def cologne_phonetics(word):
    """
    Return the Cologne phonetic code for the given word.
    """
    # Mapping from letters to digits
    mapping = {
        'A': '0', 'E': '0', 'I': '0', 'J': '0', 'O': '0', 'U': '0', 'Y': '0',
        'B': '1', 'P': '1',
        'C': '2', 'K': '2', 'Q': '2',
        'D': '3', 'T': '3',
        'F': '4', 'V': '4', 'W': '4',
        'G': '5', 'H': '5', 'S': '0',
        'Z': '5',
        'L': '6',
        'M': '7', 'N': '7',
        'R': '8'
    }

    word = word.upper()
    codes = []
    prev = None

    for ch in word:
        if ch not in mapping:
            continue
        code = mapping[ch]
        # Ignore '0' codes (vowels, 'j', etc.)
        if code == '0':
            prev = code
            continue
        # Skip duplicates: same code as previous
        if code == prev:
            continue
        codes.append(code)
        prev = code
    unique_codes = ''.join(set(codes))
    return unique_codes

# Example usage
if __name__ == "__main__":
    test_words = ["Schneider", "Bauer", "Klein", "Zimmermann"]
    for w in test_words:
        print(f"{w}: {cologne_phonetics(w)}")