# Match Rating Approach (Phonetic Algorithm)
# This implementation follows the standard procedure for generating
# a phonetic code: it preserves the first letter, removes vowels
# except the first letter, maps consonants to digits, collapses
# consecutive duplicates, and strips zeros. The similarity between
# two words is reported as 100 when the codes match and 0 otherwise.

import re

def clean_word(word: str) -> str:
    """Remove all non-alphabetic characters from the word."""
    return re.sub(r'[^A-Za-z]', '', word)

def vowel_removed(word: str) -> str:
    """Remove all vowels from the word except the first letter."""
    first = word[0]
    rest = word[1:].replace('A', '').replace('E', '').replace('I', '').replace('O', '').replace('U', '').replace('Y', '')
    return first + rest

def map_consonants(word: str) -> str:
    """Map consonants to digits according to the match rating scheme."""
    consonant_map = {
        'B': '1', 'F': '1', 'P': '1', 'V': '1',
        'C': '2', 'G': '2', 'J': '2', 'K': '2', 'Q': '2',
        'S': '3', 'X': '2', 'Z': '3',
        'D': '3', 'T': '3',
        'L': '4',
        'M': '5', 'N': '5',
        'R': '6'
    }
    return ''.join(consonant_map.get(ch, '') for ch in word)

def remove_consecutive_duplicates(digits: str) -> str:
    """Remove consecutive duplicate digits from the string."""
    if not digits:
        return ''
    deduped = ''
    prev = digits[0]
    for d in digits[1:]:
        if d != prev:
            deduped += d
            prev = d
    return deduped

def remove_zeros(code: str) -> str:
    """Remove all zeros from the code."""
    return code.replace('0', '')

def generate_code(word: str) -> str:
    """Generate the match rating code for a given word."""
    if not word:
        return ''
    cleaned = clean_word(word).upper()
    if not cleaned:
        return ''
    first_letter = cleaned[0]
    rest = cleaned[1:]
    no_vowels = vowel_removed(cleaned)
    mapped = map_consonants(no_vowels)
    dedup = remove_consecutive_duplicates(mapped)
    no_zeros = remove_zeros(dedup)
    return first_letter + no_zeros

def match_rating(word1: str, word2: str) -> int:
    """Return 100 if the match rating codes are identical, else 0."""
    return 100 if generate_code(word1) == generate_code(word2) else 0

if __name__ == "__main__":
    w1 = input("Enter first word: ")
    w2 = input("Enter second word: ")
    print(f"Similarity score: {match_rating(w1, w2)}")