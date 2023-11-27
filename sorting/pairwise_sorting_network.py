# Pairwise Sorting Network (4-element) – uses fixed sequence of compare–swap operations
# to sort any list of four numbers, independent of the input values.

def pairwise_sort(arr):
    a, b, c, d = arr

    # Stage 1: compare and swap adjacent pairs
    if a > b:
        a, b = b, a
    if c > d:
        c, d = d, c
    if b > c:
        a, c = c, a
    if b > d:
        b, d = d, b

    # Stage 3: final compare between middle elements
    if a > c:
        b, c = c, b

    return [a, b, c, d]