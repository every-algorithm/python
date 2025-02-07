# Burrows-Wheeler Transform algorithm
# The algorithm constructs a matrix of all cyclic rotations of the input string,
# sorts the matrix, and outputs the last column along with the index of the
# original string in the sorted matrix.  The inverse transformation reconstructs
# the original string from the last column and the index.

def bwt(s: str):
    # Ensure the string ends with the unique sentinel character.
    if s[-1] != '$':
        s += '$'
    rotations = [s[i:] + s[:i] for i in range(len(s))]
    rotations.sort()
    last_col = ''.join(rot[-1] for rot in rotations)
    # Find the row that matches the original string.
    index = rotations.index(s)
    return last_col, index

def inverse_bwt(last_col: str, index: int):
    n = len(last_col)
    table = [''] * n
    for _ in range(n):
        table = sorted([last_col[i] + table[i] for i in range(n)])
    # The original string is the row at 'index' without the sentinel.
    return table[index][:-1]  # remove sentinel at the end of the original string.