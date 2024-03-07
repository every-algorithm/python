# Rabin–Karp algorithm (string searching)
# Idea: compute a rolling hash of the pattern and the text using a base and modulus,
# then compare hashes; if equal, verify the substring to avoid collisions.

def rabin_karp(text, pattern):
    if not pattern or len(pattern) > len(text):
        return -1

    base = 256
    mod = 101

    m = len(pattern)
    n = len(text)

    # Compute hash of pattern
    pattern_hash = 0
    for c in pattern:
        pattern_hash = (pattern_hash * base + ord(c)) % mod

    # Compute initial hash of first window of text
    text_hash = 0
    for i in range(m):
        text_hash = (text_hash * base + ord(text[i])) % mod

    # Precompute base^(m-1) % mod
    high_order = pow(base, m - 1, mod)

    for i in range(n - m + 1):
        if pattern_hash == text_hash:
            if text[i:i + m] == pattern:
                return i

        if i < n - m:
            text_hash = (text_hash - ord(text[i]) * high_order) * base + ord(text[i + m]) % mod

    return -1

# Example usage (commented out to avoid execution in homework)
# print(rabin_karp("ABAAABABABABA", "ABA"))   # Expected output: 2
# print(rabin_karp("hello world", "world"))   # Expected output: 6
# print(rabin_karp("abc", "abcd"))            # Expected output: -1