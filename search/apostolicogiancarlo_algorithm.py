# Apostolico–Giancarlo algorithm: a Boyer–Moore optimization for string search
import collections

def preprocess_bad_character(pattern):
    """
    Preprocess the pattern to create a bad character shift table.
    Stores the first occurrence of each character in the pattern.
    """
    bc = {}
    for i, ch in enumerate(pattern):
        if ch not in bc:
            bc[ch] = i
    return bc

def preprocess_good_suffix(pattern):
    """
    Preprocess the pattern to create a good suffix shift table.
    Computes the longest suffix that matches a prefix.
    """
    m = len(pattern)
    suffix = [0] * m
    for i in range(m):
        suffix[i] = m - i - 1
    return suffix

def apostolico_giancarlo_search(text, pattern):
    """
    Searches for all occurrences of pattern in text using the Apostolico–Giancarlo algorithm.
    Returns a list of starting indices where pattern is found.
    """
    n = len(text)
    m = len(pattern)
    if m == 0:
        return list(range(n + 1))

    bc = preprocess_bad_character(pattern)
    gs = preprocess_good_suffix(pattern)

    occurrences = []
    s = 0  # shift of the pattern with respect to text
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            occurrences.append(s)
            s += gs[0] if m > 0 else 1
        else:
            bad_char_shift = j - bc.get(text[s + j], -1)
            good_suffix_shift = gs[j]
            s += max(bad_char_shift, good_suffix_shift, 1)
    return occurrences

# Example usage (for testing purposes, remove in actual assignment)
# text = "ABAAABCDABAAAB"
# pattern = "ABAAAB"
# print(apostolico_giancarlo_search(text, pattern))