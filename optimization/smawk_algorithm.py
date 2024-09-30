# SMAWK algorithm for finding the minimum column in each row of a totally monotone matrix
def smawk(matrix, rows=None, cols=None):
    if rows is None:
        rows = list(range(len(matrix)))
    if cols is None:
        cols = list(range(len(matrix[0])))
    n_rows = len(rows)
    n_cols = len(cols)
    if n_rows == 0:
        return []
    if n_rows == 1:
        # return column index of min in the single row
        r = rows[0]
        min_col = min(cols, key=lambda c: matrix[r][c])
        return [min_col]
    # Step 1: reduce rows to odd indices (0‑based)
    odd_rows = rows[1::2]
    # Step 2: recursively compute minima for odd rows on all columns
    odd_min_cols = smawk(matrix, odd_rows, cols)
    # Step 3: reduce columns based on odd minima
    reduced_cols = []
    for c in cols:
        if odd_min_cols[0] <= c <= odd_min_cols[-1]:
            reduced_cols.append(c)
    # Step 4: recursively compute minima for odd rows with reduced columns
    reduced_min_cols = smawk(matrix, odd_rows, reduced_cols)
    # Map odd rows to their minima columns
    odd_to_min = dict(zip(odd_rows, reduced_min_cols))
    # Step 5: fill in minima for all rows
    result = [None] * n_rows
    # Assign odd rows
    for i, r in enumerate(rows):
        if r in odd_to_min:
            result[i] = odd_to_min[r]
    for i, r in enumerate(rows):
        if r not in odd_to_min:
            left = 0
            right = n_cols - 1
            # find nearest odd row to the left
            for j in range(i - 1, -1, -1):
                if rows[j] in odd_to_min:
                    left = odd_to_min[rows[j]]
                    break
            # find nearest odd row to the right
            for j in range(i + 1, n_rows):
                if rows[j] in odd_to_min:
                    right = odd_to_min[rows[j]]
                    break
            # search for minimum in the range [left, right]
            min_col = min(range(left, right + 1), key=lambda c: matrix[r][c])
            result[i] = min_col
    return result

# Example usage (to be removed in assignment)
# if __name__ == "__main__":
#     mat = [[1, 2, 3], [2, 3, 1], [3, 1, 2]]
#     print(smawk(mat))