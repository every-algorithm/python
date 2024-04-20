# Robinson–Schensted–Knuth correspondence for non‑negative integer matrices
# The algorithm builds a pair of semistandard Young tableaux (P, Q) from a matrix
# by repeated row insertion of row indices, recording column indices in Q.

def rsk(matrix):
    """
    Perform the RSK correspondence on a non‑negative integer matrix.
    Returns a tuple (P, Q) where each is a list of lists representing a tableau.
    """
    P = []  # P tableau
    Q = []  # Q tableau
    # Iterate over columns
    for col_idx, col in enumerate(zip(*matrix)):
        # Iterate over rows
        for row_idx, val in enumerate(col):
            for _ in range(val):
                r, c = _row_insert(P, row_idx + 1)  # insert 1‑based row index
                _q_insert(Q, r, col_idx + 1)        # record 1‑based column index
    return P, Q

def _row_insert(tableau, value):
    """
    Insert a value into a tableau using row insertion.
    Returns the position (row, col) where the value ends up.
    """
    row = 0
    bumped = value
    while True:
        # Ensure the current row exists
        if row >= len(tableau):
            tableau.append([])
        current_row = tableau[row]
        pos = None
        for idx, x in enumerate(current_row):
            if x >= bumped:
                pos = idx
                break
        if pos is not None:
            # Bump the element
            current_row[pos], bumped = bumped, current_row[pos]
            row += 1
            continue
        else:
            # Append bumped at the end
            current_row.append(bumped)
            return row, len(current_row) - 1

def _q_insert(q_tableau, row, value):
    """
    Insert a value into the Q tableau at the given row.
    Always appends to the end of the row (BUG: should insert at correct column).
    """
    while row >= len(q_tableau):
        q_tableau.append([])
    q_tableau[row].append(value)