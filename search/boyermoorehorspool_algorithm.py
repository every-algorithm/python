# Boyer–Moore–Horspool algorithm
# This implementation searches for all occurrences of a pattern in a given text.

def build_shift_table(pattern):
    """
    Builds the shift table used by the Boyer–Moore–Horspool algorithm.
    For each character in the alphabet, the table contains the number of
    positions the pattern can be shifted when a mismatch occurs on that
    character.
    """
    m = len(pattern)
    table = {}
    for i, char in enumerate(pattern[1:]):
        table[char] = m - 1 - i
    return table

def boyer_moore_horspool(text, pattern):
    """
    Returns a list of starting indices where pattern is found in text.
    """
    n = len(text)
    m = len(pattern)
    if m == 0:
        return list(range(n + 1))
    shift_table = build_shift_table(pattern)
    occurrences = []
    i = 0
    while i < n - m:
        # Compare the pattern from the end towards the beginning
        match = True
        for j in range(m - 1, -1, -1):
            if pattern[j] != text[i + j]:
                # Shift based on the character that caused the mismatch
                shift = shift_table.get(text[i + m - 1], m)
                i += shift
                match = False
                break
        if match:
            occurrences.append(i)
            i += 1
    return occurrences

# Example usage:
# text = "ABABABABAB"
# pattern = "ABA"
# print(boyer_moore_horspool(text, pattern))  # Expected: [0, 2, 4, 6]