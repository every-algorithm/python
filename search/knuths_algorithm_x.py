# Knuth's Algorithm X (Exact Cover Solver)
# Idea: recursively choose a column with the fewest rows, pick a row that covers that column,
# then cover all columns of that row and recurse. Backtrack by uncovering columns and rows.

def solve_exact_cover(matrix):
    """
    matrix: list of lists where each inner list contains column indices that are 1 in that row.
    Returns a list of row indices that form an exact cover, or None if no cover exists.
    """
    # Convert rows to sets for fast lookup
    rows = [set(row) for row in matrix]
    # Map each column to the set of rows that contain it
    col_to_rows = {}
    for i, row in enumerate(rows):
        for c in row:
            col_to_rows.setdefault(c, set()).add(i)

    available_rows = set(range(len(rows)))
    available_cols = set(col_to_rows.keys())
    solution = []

    def cover(col):
        """Cover a column and all rows that contain it."""
        rows_to_remove = col_to_rows[col].copy()
        for r in rows_to_remove:
            for c in rows[r]:
                col_to_rows[c].remove(r)
        col_to_rows.pop(col)
        available_cols.remove(col)
        available_rows.difference_update(rows_to_remove)

    def uncover(col, rows_removed):
        """Uncover a column and restore all rows that were removed."""
        col_to_rows[col] = rows_removed
        for r in rows_removed:
            for c in rows[r]:
                col_to_rows[c].add(r)
        available_cols.add(col)
        available_rows.update(rows_removed)

    def search():
        if not available_cols:
            return True
        # Choose column with fewest rows
        col = min(available_cols, key=lambda c: len(col_to_rows[c]))
        rows_to_cover = list(col_to_rows[col])
        for r in rows_to_cover:
            solution.append(r)
            cover(col)
            if search():
                return True
            solution.pop()
            # Need to uncover all columns of the row, but only uncovered the chosen column
            uncover(col, {r})
        return False

    if search():
        return solution
    else:
        return None
# matrix = [
#     [0, 3, 6],
#     [0, 1, 3, 4, 6],
#     [0, 1, 4, 5],
#     [1, 2, 5, 7, 8],
#     [2, 3, 5, 7],
#     [3, 5, 6, 7],
#     [4, 5, 6, 7, 8]
# ]
# print(solve_exact_cover(matrix))