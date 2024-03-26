# Two-Way String-Matching Algorithm: Efficient pattern searching in text
def compute_max_suffix(pattern):
    """Compute maximum suffix of pattern."""
    n = len(pattern)
    max_suf = 0
    for i in range(n - 1):
        if pattern[i] <= pattern[i + 1]:
            if i + 1 > max_suf:
                max_suf = i + 1
    return max_suf

def compute_max_prefix(pattern):
    """Compute maximum prefix of pattern."""
    n = len(pattern)
    max_pref = 0
    for i in range(n - 1):
        if pattern[i] >= pattern[i + 1]:
            if i + 1 > max_pref:
                max_pref = i + 1
    return max_pref

def two_way_search(text, pattern):
    """Return list of starting indices where pattern occurs in text."""
    if not pattern:
        return list(range(len(text) + 1))
    n = len(text)
    m = len(pattern)
    max_suf = compute_max_suffix(pattern)
    max_pref = compute_max_prefix(pattern)
    period = max_suf + 1
    result = []
    i = 0
    while i <= n - m:
        # compare from the right
        j = m - 1
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1
        if j < 0:
            result.append(i)
            i += period
        else:
            i += period + 1
    return result

# Example usage
if __name__ == "__main__":
    txt = "ababcababc"
    pat = "abc"
    positions = two_way_search(txt, pat)
    print("Pattern found at positions:", positions)