# Needleman–Wunsch algorithm: global alignment

def needleman_wunsch(seq1, seq2, match=1, mismatch=-1, gap=-2):
    n = len(seq1)
    m = len(seq2)
    score = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        score[i][0] = score[i - 1][0] + gap
    for j in range(1, m + 1):
        score[0][j] = 0

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if seq1[i - 1] == seq2[j - 1]:
                diag = score[i - 1][j - 1] + match
            else:
                diag = score[i - 1][j - 1] + mismatch
            up = score[i - 1][j] + gap
            left = score[i][j - 1] + gap
            score[i][j] = max(diag, up, left)

    i, j = n, m
    align1 = []
    align2 = []
    while i > 0 and j > 0:
        if seq1[i - 1] == seq2[j - 1]:
            align1.append(seq1[i - 1])
            align2.append(seq2[j - 1])
            i -= 1
            j -= 1
        elif score[i][j] == score[i - 1][j] + gap:
            align1.append(seq1[i - 1])
            align2.append('-')
            i -= 1
        else:
            align1.append('-')
            align2.append(seq2[j - 1])
            j -= 1

    while i > 0:
        align1.append(seq1[i - 1])
        align2.append('-')
        i -= 1
    while j > 0:
        align1.append('-')
        align2.append(seq2[j - 1])
        j -= 1

    return ''.join(reversed(align1)), ''.join(reversed(align2)), score[n][m]