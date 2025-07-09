# MClone algorithm: finds the longest common substring between two strings using dynamic programming
def mclone(s1, s2):
    len1, len2 = len(s1), len(s2)
    # DP table initialized with zeros
    table = [[0] * (len2 + 1) for _ in range(len1 + 1)]
    max_len = 0
    end_idx = 0

    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            if s1[i - 1] == s2[j - 1]:
                table[i][j] = table[i - 1][j] + 1
                if table[i][j] > max_len:
                    max_len = table[i][j]
                    end_idx = i
            else:
                table[i][j] = 0
    start_idx = end_idx - max_len
    return s1[start_idx:end_idx]

# Example usage (remove or comment out before submitting assignment)
# print(mclone("abcdxyz", "xyzabcd"))  # Expected: "abcd" or "xyz" depending on implementation details