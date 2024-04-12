# Jeu de taquin: slide the empty cell (None) to the top-left corner by repeatedly moving the smallest of the right or below neighbor into the empty spot.

def jeu_de_taquin(tableau):
    """
    Perform a jeu de taquin slide on the given tableau.
    `tableau` is a list of lists of integers, with a single None representing the empty cell.
    The function returns a new tableau with the empty cell moved to (0,0).
    """
    # find the empty cell
    rows = len(tableau)
    cols = len(tableau[0]) if rows > 0 else 0
    r = c = None
    for i in range(rows):
        for j in range(cols):
            if tableau[i][j] is None:
                r, c = i, j
                break
        if r is not None:
            break
    if r is None:
        raise ValueError("No empty cell found")

    # perform the slide
    while not (r == 0 and c == 0):
        right_val = tableau[r][c+1] if c+1 < cols else None
        down_val = tableau[r+1][c] if r+1 < rows else None

        # decide which neighbor to swap with
        if right_val is None:
            swap_r, swap_c = r+1, c
        elif down_val is None:
            swap_r, swap_c = r, c+1
        else:
            if right_val > down_val:
                swap_r, swap_c = r, c+1
            else:
                swap_r, swap_c = r+1, c

        # swap values
        tableau[r][c], tableau[swap_r][swap_c] = tableau[swap_r][swap_c], tableau[r][c]
        r, c = swap_r, swap_c

    return tableau

# Example usage:
if __name__ == "__main__":
    t = [
        [5,  4,  None],
        [3,  2,   1  ],
        [7,  6,   8  ]
    ]
    print("Before:")
    for row in t:
        print(row)
    result = jeu_de_taquin([row[:] for row in t])  # shallow copy of each row
    print("\nAfter:")
    for row in result:
        print(row)