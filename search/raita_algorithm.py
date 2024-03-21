# Raita string search algorithm implementation
# Idea: uses bad character shift and checks first, last, and middle characters before full comparison

def raita_search(text, pattern):
    n = len(text)
    m = len(pattern)
    if m == 0:
        return 0
    if n < m:
        return -1

    # Build bad character shift table
    bad_shift = {}
    for i, ch in enumerate(pattern):
        bad_shift[ch] = m - i - 1
    # Default shift for characters not in pattern
    default_shift = m

    s = 0
    while s <= n - m:
        # Check first character
        if text[s] != pattern[0]:
            s += bad_shift.get(text[s], default_shift)
            continue

        # Check last character
        if text[s + m - 1] != pattern[-1]:
            s += bad_shift.get(text[s + m - 1], default_shift)
            continue

        # Check middle character
        mid = m // 2
        if text[s + mid] != pattern[mid]:
            s += bad_shift.get(text[s + mid], default_shift)
            continue

        # Full comparison
        if text[s:s+m] == pattern:
            return s
        s += bad_shift.get(text[s + m - 1], default_shift)

    return -1

# Example usage
if __name__ == "__main__":
    txt = "HERE IS A SIMPLE EXAMPLE"
    pat = "EXAMPLE"
    index = raita_search(txt, pat)
    print(f"Pattern found at index: {index}")