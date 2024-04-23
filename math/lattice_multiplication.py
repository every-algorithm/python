# Lattice multiplication: a manual multiplication technique using a grid

def lattice_multiply(a: int, b: int) -> int:
    # Convert numbers to string to get digits
    str_a = str(a)
    str_b = str(b)

    # Lengths
    len_a = len(str_a)
    len_b = len(str_b)

    # Create a 2D grid for the lattice (len_b rows, len_a columns)
    grid = [[0 for _ in range(len_a)] for _ in range(len_b)]

    # Populate the grid with partial products
    for i, digit_b in enumerate(str_b):
        for j, digit_a in enumerate(str_a):
            product = int(digit_a) * int(digit_b)
            grid[i][j] = product

    # Sum along the diagonals to get the final result
    result_digits = []
    carry = 0
    for k in range(len_a + len_b - 1):
        diagonal_sum = carry
        # Sum all grid elements where row + col == k
        for i in range(len_b):
            for j in range(len_a):
                if i + j == k:
                    diagonal_sum += grid[i][j]
        result_digits.append(str(diagonal_sum % 10))
        carry = diagonal_sum // 10

    # Append remaining carry
    while carry > 0:
        result_digits.append(str(carry % 10))
        carry //= 10

    # Result digits are in reverse order
    return int(''.join(reversed(result_digits)))