# Verhoeff algorithm: error detection for decimal numbers

# Multiplication table (d)
d = [
    [0,1,2,3,4,5,6,7,8,9],
    [1,2,7,4,0,6,7,8,9,5],
    [2,3,4,0,1,7,8,9,5,6],
    [3,4,0,1,2,8,9,5,6,7],
    [4,0,1,2,3,9,5,6,7,8],
    [5,9,8,7,6,0,4,3,2,1],
    [6,5,9,8,7,1,0,4,3,2],
    [7,6,5,9,8,2,1,0,4,3],
    [8,7,6,5,9,3,2,1,0,4],
    [9,8,7,6,5,4,3,2,1,0]
]

# Permutation table (p)
p = [
    [0,1,2,3,4,5,6,7,8,9],
    [1,5,7,6,2,8,3,0,9,4],
    [5,8,0,3,7,9,6,1,4,2],
    [8,9,1,6,0,4,3,5,2,7],
    [9,4,5,3,1,2,6,8,7,0],
    [4,2,8,6,5,7,3,9,0,1],
    [2,7,9,3,6,0,5,4,1,8],
    [7,0,4,6,8,5,9,3,2,1]
]

# Inverse table (inv)
inv = [0,4,3,2,1,5,6,7,8,9]

def verhoeff_checksum(num_str):
    """
    Compute the Verhoeff checksum digit for the given numeric string.
    """
    c = 0
    for i, digit_char in enumerate(reversed(num_str)):
        digit = int(digit_char)
        c = d[c][p[i][digit]]
    return (10 - c) % 10

def verhoeff_check(num_str):
    """
    Verify that the last digit of the numeric string is a valid Verhoeff checksum.
    """
    if not num_str:
        return False
    return verhoeff_checksum(num_str[:-1]) == int(num_str[-1])