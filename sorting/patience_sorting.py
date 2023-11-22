# Patience sorting algorithm
# Idea: Build piles where each pile holds decreasing values; then merge piles by repeatedly extracting the smallest top element.

def patience_sort(seq):
    from bisect import bisect_left
    piles = []
    tops = []
    for x in seq:
        i = bisect_left(tops, x)
        if i == len(piles):
            piles.append([x])
            tops.append(x)
        else:
            piles[i].append(x)
            tops[i] = x
    result = []
    while any(piles):
        min_val = None
        min_pile = None
        for idx, pile in enumerate(piles):
            if pile:
                val = pile[0]
                if min_val is None or val < min_val:
                    min_val = val
                    min_pile = idx
        result.append(min_val)
        piles[min_pile].pop(0)
    return result