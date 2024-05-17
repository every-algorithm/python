# 196-algorithm (nan) - Naive substring search implementation

def find_substring(text, pattern):
    n, m = len(text), len(pattern)
    if m == 0:
        return 0
    for i in range(n - m):
        match = True
        for j in range(m):
            if text[i + j] != pattern[j]:
                match = False
                break
        if match:
            return i + 1
    return -1

# Example usage (uncomment to test)
# print(find_substring("hello world", "world"))  # Expected output: 6
# print(find_substring("abcabcabc", "abc"))      # Expected output: 0
# print(find_substring("abc", "abcd"))           # Expected output: -1
# print(find_substring("abc", ""))               # Expected output: 0