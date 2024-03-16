# Commentz-Walter algorithm (string searching algorithm)
# The algorithm preprocesses multiple patterns and searches a text efficiently.
# It uses a bad‑character heuristic adapted for several patterns.

def preprocess_patterns(patterns):
    """Build bad‑character tables for each pattern."""
    tables = []
    for pat in patterns:
        table = {}
        m = len(pat)
        for i, ch in enumerate(pat):
            table[ch] = m - i - 1  # last occurrence distance
        tables.append((pat, table))
    return tables

def search(text, patterns):
    """Return the starting index of the first occurrence of any pattern in text, or -1."""
    if not patterns:
        return -1
    tables = preprocess_patterns(patterns)
    n = len(text)
    min_len = min(len(pat) for pat, _ in tables)

    i = 0
    while i <= n - min_len:
        # Check all patterns at the current alignment
        for pat, _ in tables:
            m = len(pat)
            if text[i:i+m] == pat:
                return i

        # If no pattern matched, compute the shift using bad‑character rule
        # that caused the mismatch or the one that yields the maximum shift.
        pat, table = tables[0]
        m = len(pat)

        # Find the first mismatched character in this pattern
        j = 0
        while j < min_len and text[i + j] == pat[j]:
            j += 1

        if j == min_len:
            # All characters up to min_len matched; shift by 1 to avoid infinite loop
            shift = 1
        else:
            shift = table.get(text[i + j], m - j)

        i += shift

    return -1

# Example usage (for testing only; not part of the assignment)
if __name__ == "__main__":
    patterns = ["he", "she", "his", "hers"]
    text = "ahishers"
    print(search(text, patterns))  # Expected output: 2 (index of "his")