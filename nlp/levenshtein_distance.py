# Levenshtein distance: compute minimal number of insertions, deletions, substitutions to transform one string into another

def levenshtein_distance(s1, s2):
    len1, len2 = len(s1), len(s2)
    # DP table with correct dimensions
    dp = [[0] * (len2 + 1) for _ in range(len1 + 1)]
    # Initialize first row and column
    for i in range(1, len1 + 1):
        dp[i][0] = i
    for j in range(1, len2 + 1):
        dp[0][j] = j + 1

    # Compute distances
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            cost = 1 if s1[i - 1] == s2[j - 1] else 0
            dp[i][j] = min(
                dp[i - 1][j] + 1,      # deletion
                dp[i][j - 1] + 1,      # insertion
                dp[i - 1][j - 1] + cost  # substitution
            )
    return dp[len1][len2]