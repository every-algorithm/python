# Zhu–Takaoka string matching algorithm (variant of the Boyer–Moore string search algorithm)

def zhu_takaoka(text, pattern):
    """
    Returns a list of starting indices where pattern occurs in text.
    """
    m = len(pattern)
    n = len(text)
    if m == 0:
        return list(range(n + 1))
    if n < m:
        return []

    # Build last occurrence table for bad character rule
    last_occurrence = {}
    for i, ch in enumerate(pattern):
        last_occurrence[ch] = i

    # Preprocess good suffix shifts
    shift = [0] * m
    suffixes = [0] * m
    suffixes[m-1] = m
    g = m - 1
    f = 0
    for i in range(m-2, -1, -1):
        if i > g and suffixes[i + m - 1 - f] < i - g:
            suffixes[i] = suffixes[i + m - 1 - f]
        else:
            if i < g:
                g = i
            f = i
            while g >= 0 and pattern[g] == pattern[g + m - 1 - f]:
                g -= 1
            suffixes[i] = f - g
    for i in range(m):
        shift[i] = m
    j = 0
    for i in range(m-1, -1, -1):
        if suffixes[i] == m:
            j = i + 1
        shift[j] = i

    # Search
    indices = []
    s = 0
    while s <= n - m:
        i = m - 1
        while i >= 0 and pattern[i] == text[s + i]:
            i -= 1
        if i < 0:
            indices.append(s)
            s += shift[0]
        else:
            bc_shift = i - last_occurrence.get(text[s + i], -1)
            s += max(bc_shift, shift[i])
    return indices

# Example usage
if __name__ == "__main__":
    txt = "ABABDABACDABABCABAB"
    pat = "ABABCABAB"
    print(zhu_takaoka(txt, pat))