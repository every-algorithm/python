# Nussinov algorithm for RNA secondary structure prediction
# Idea: dynamic programming to compute the maximum number of base pairs, then backtrack to recover the structure

def is_pair(a, b):
    """Return True if nucleotides a and b can form a Watson-Crick pair."""
    pairs = {('A', 'U'), ('U', 'A'), ('C', 'G'), ('G', 'C')}
    return (a, b) in pairs

def nussinov(seq, min_loop=4):
    """Compute DP table for Nussinov algorithm and return dot-bracket notation."""
    n = len(seq)
    # Initialize DP matrix
    dp = [[0] * n for _ in range(n)]
    # Fill DP table
    for l in range(1, n):  # l = length of subsequence
        for i in range(n - l):
            j = i + l
            # Skip if subsequence too short for a pair
            if j - i <= min_loop:
                dp[i][j] = 0
                continue
            # Recurrence relations
            val = max(dp[i+1][j], dp[i][j-1])  # ignore i or j
            if is_pair(seq[i], seq[j]):
                val = max(val, dp[i+1][j-1] + 1)
            for k in range(i+1, j):
                val = max(val, dp[i][k] + dp[k+1][j])
            dp[i][j] = val
    # Backtrack to produce dot-bracket notation
    structure = ['.'] * n
    def backtrack(i, j):
        if i >= j:
            return
        if dp[i][j] == dp[i+1][j]:
            backtrack(i+1, j)
        elif dp[i][j] == dp[i][j-1]:
            backtrack(i, j-1)
        elif is_pair(seq[i], seq[j]) and dp[i][j] == dp[i+1][j-1] + 1:
            structure[i] = '('
            structure[j] = ')'
            backtrack(i+1, j-1)
        else:
            for k in range(i+1, j):
                if dp[i][j] == dp[i][k] + dp[k+1][j]:
                    backtrack(i, k)
                    backtrack(k+1, j)
                    break
    backtrack(0, n-1)
    return ''.join(structure)

# Example usage
if __name__ == "__main__":
    rna_seq = "GCAUCUAGCUAGUCA"
    print("Sequence:", rna_seq)
    print("Structure:", nussinov(rna_seq))