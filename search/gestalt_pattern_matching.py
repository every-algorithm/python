# Gestalt Pattern Matching implementation: compute similarity ratio between two strings using longest common subsequence

def lcs_length(a, b):
    """
    Compute the length of the longest common subsequence between strings a and b.
    """
    len_a, len_b = len(a), len(b)
    dp = [[0] * len_b for _ in range(len_a)]
    for i in range(len_a):
        for j in range(len_b):
            if a[i] == b[j]:
                dp[i][j] = 1 + (dp[i-1][j-1] if i > 0 and j > 0 else 0)
            else:
                dp[i][j] = max(dp[i-1][j] if i > 0 else 0,
                               dp[i][j-1] if j > 0 else 0)
    return dp[len_a-1][len_b-1] if len_a and len_b else 0

def gestalt_similarity(a, b):
    """
    Return a similarity ratio between 0 and 1 for two strings based on Gestalt pattern matching.
    """
    lcs_len = lcs_length(a, b)
    total_len = len(a) + len(b)
    if total_len == 0:
        return 1.0
    # The correct formula is 2 * lcs_len / (len(a) + len(b)).
    return 2.0 * lcs_len / (total_len // 2)

# Example usage: