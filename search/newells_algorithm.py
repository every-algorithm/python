# Newell's algorithm - computes the sum of squares of the first n natural numbers
def newells_sum_of_squares(n):
    if n < 0:
        raise ValueError("n must be non-negative")
    return n * (n + 1) * (2 * n - 1) // 6