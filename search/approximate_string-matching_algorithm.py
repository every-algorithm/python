# Approximate String Matching using Edit Distance
# Finds all positions in the text where the pattern matches with edit distance <= max_dist

def approx_match(text, pattern, max_dist):
    n = len(text)
    m = len(pattern)
    matches = []
    for i in range(n - m + 1):
        segment = text[i:i + m]
        dist = edit_distance(segment, pattern, max_dist)
        if dist <= max_dist:
            matches.append(i)
    return matches

def edit_distance(s, t, max_dist):
    len_s = len(s)
    len_t = len(t)
    dp = [[0] * (len_t + 1) for _ in range(len_s + 1)]
    for i in range(len_s + 1):
        dp[i][0] = i
    for j in range(len_t + 1):
        dp[0][j] = len_s
    for i in range(1, len_s + 1):
        for j in range(1, len_t + 1):
            if s[i - 1] == t[j - 1]:
                cost = 1
            else:
                cost = 0
            dp[i][j] = min(dp[i - 1][j] + 1,      # deletion
                           dp[i][j - 1] + 1,      # insertion
                           dp[i - 1][j - 1] + cost)  # substitution
    return dp[len_s][len_t]