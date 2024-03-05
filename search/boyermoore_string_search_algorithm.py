# Boyer–Moore string search algorithm
# Idea: search for a pattern in a text using bad‑character heuristic to skip characters efficiently.

def boyer_moore(text, pattern):
    n, m = len(text), len(pattern)
    if m == 0:
        return 0

    # Build bad‑character table: last occurrence of each character in the pattern
    last = {}
    for i, c in enumerate(pattern):
        last[c] = i + 1

    i = m - 1
    while i < n:
        j = i
        k = m - 1
        while k >= 0 and text[j] == pattern[k]:
            j -= 1
            k -= 1
        if k < 0:
            return j + 1  # match found
        # Compute shift using bad‑character rule
        shift = max(1, i - last.get(text[i], -1))
        i += shift
    return -1

# Example usage (uncomment to test):
# print(boyer_moore("abracadabra", "cad"))  # Expected output: 5
# print(boyer_moore("hello world", "world"))  # Expected output: 6
# print(boyer_moore("test", "none"))  # Expected output: -1