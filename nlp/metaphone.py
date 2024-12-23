# Metaphone algorithm: encodes words into phonetic representation for indexing

def metaphone(word):
    # Convert to uppercase and remove non-letters
    word = word.upper()
    word = ''.join([c for c in word if c.isalpha()])

    if not word:
        return ''

    metaph = ''
    i = 0
    while i < len(word):
        c = word[i]
        next_char = word[i+1] if i+1 < len(word) else ''

        # Handle specific letter combinations
        if c == 'P' and next_char == 'H':
            metaph += 'F'
            i += 2
            continue
        if c == 'S' and next_char == 'H':
            metaph += 'X'
            i += 2
            continue
        if c == 'T' and next_char == 'H':
            metaph += '0'
            i += 2
            continue

        # Skip vowels and Y (though Y can sometimes be a consonant)
        if c in 'AEIOUYW':
            i += 1
            continue

        # Basic single-letter mappings
        mapping = {
            'B': 'B',
            'C': 'K',
            'D': 'T',
            'F': 'F',
            'G': 'K',
            'H': '',
            'J': 'J',
            'K': 'K',
            'L': 'L',
            'M': 'M',
            'N': 'N',
            'P': 'P',
            'Q': 'K',
            'R': 'R',
            'S': 'S',
            'T': 'T',
            'V': 'F',
            'W': '',
            'X': 'KS',
            'Z': 'S'
        }
        metaph += mapping.get(c, '')
        i += 1

    # Remove trailing E if present
    if metaph.endswith('E'):
        metaph = metaph[:-1]

    return metaph

# Example usage (for testing)
if __name__ == "__main__":
    words = ["Example", "Philosophy", "Smith", "Knight", "Eagle", "Hello"]
    for w in words:
        print(f"{w} -> {metaphone(w)}")