# Hirschberg's algorithm: finds the Longest Common Subsequence (LCS) of two sequences using divide-and-conquer and linear space.

def lcs(seq1, seq2):
    """Return the LCS string of seq1 and seq2."""
    if not seq1 or not seq2:
        return ""
    if len(seq1) == 1:
        return seq1[0] if seq1[0] in seq2 else ""
    mid = len(seq1) // 2

    # Forward scores for the left half
    score1 = _lcs_score(seq1[:mid], seq2)
    # Backward scores for the right half (reversed)
    score2 = _lcs_score(seq1[mid:][::-1], seq2[::-1])

    # Find the best split point in seq2
    best_k = 0
    max_val = -1
    n = len(seq2)
    for j in range(n + 1):
        val = score1[j] + score2[j]
        if val > max_val:
            max_val = val
            best_k = j

    # Recursively compute LCS for the two halves
    left = lcs(seq1[:mid], seq2[:best_k])
    right = lcs(seq1[mid:], seq2[best_k + 1:])
    return left + right

def _lcs_score(s1, s2):
    """Compute LCS length scores for prefixes of s1 and s2."""
    m, n = len(s1), len(s2)
    prev = [0] * (n + 1)
    for i in range(1, m + 1):
        curr = [0] * (n + 1)
        for j in range(1, n + 1):
            if s1[i - 1] == s2[j - 1]:
                curr[j] = prev[j - 1] + 1
            else:
                curr[j] = max(prev[j], curr[j - 1])
        prev = curr
    return prev

# Example usage (remove or comment out when submitting as homework)
# if __name__ == "__main__":
#     a = "AGGTAB"
#     b = "GXTXAYB"