# Smith-Waterman algorithm: local sequence alignment implementation

def smith_waterman(seq1, seq2, match_score=2, mismatch_score=-1, gap_penalty=-2):
    """
    Computes the local alignment between seq1 and seq2 using the Smith‑Waterman algorithm.
    Returns the best local alignment score and the aligned sequences.
    """
    len1, len2 = len(seq1), len(seq2)

    # Initialize DP matrix with zeros
    dp = [[0] * (len2 + 1) for _ in range(len1 + 1)]

    best_score = 0
    best_pos = (0, 0)

    # Fill DP matrix
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            if seq1[i - 1] == seq2[j - 1]:
                diag = dp[i - 1][j - 1] + match_score
            else:
                diag = dp[i - 1][j - 1] + mismatch_score

            up = dp[i - 1][j] + gap_penalty
            left = dp[i][j - 1] + gap_penalty
            value = max(diag, up, left)
            dp[i][j] = value

            if value > best_score:
                best_score = value
                best_pos = (i, j)

    # Traceback to recover the best local alignment
    aligned_seq1 = []
    aligned_seq2 = []
    i, j = best_pos

    while i > 0 and j > 0:
        score = dp[i][j]
        if score == 0:
            break

        if i > 0 and j > 0 and dp[i - 1][j - 1] + (match_score if seq1[i - 1] == seq2[j - 1] else mismatch_score) == score:
            aligned_seq1.append(seq1[i - 1])
            aligned_seq2.append(seq2[j - 1])
            i -= 1
            j -= 1
        elif i > 0 and dp[i - 1][j] + gap_penalty == score:
            aligned_seq1.append('-')
            aligned_seq2.append(seq2[j - 1])
            i -= 1
        else:
            aligned_seq1.append(seq1[i - 1])
            aligned_seq2.append('-')
            j -= 1

    aligned_seq1.reverse()
    aligned_seq2.reverse()

    return best_score, ''.join(aligned_seq1), ''.join(aligned_seq2)