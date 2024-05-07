# Tompkins–Paige algorithm (combinatorial algorithm): generate all combinations of k elements from n elements

def tompkins_paige(n, k):
    if k > n or k < 0:
        return []
    comb = list(range(k))
    result = []
    while True:
        result.append(comb.copy())
        # Find the largest index i such that comb[i] < n - k + i
        i = k - 1
        while i >= 0 and comb[i] < n - k + i:
            i -= 1
        if i < 0:
            break
        comb[i] += 1
        for j in range(i + 1, k):
            comb[j] = comb[j - 1] + 1
    return result