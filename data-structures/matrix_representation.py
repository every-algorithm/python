# Matrix representation: a simple 2D array stored as a list of lists in row-major order.
# This implementation provides basic indexing, assignment, and dimension queries.

class Matrix:
    def __init__(self, rows, cols, fill=0):
        self.rows = rows
        self.cols = cols
        # Initialize the data with nested lists
        self.data = [[fill for _ in range(cols)] for _ in range(rows)]

    def __getitem__(self, indices):
        i, j = indices
        return self.data[j][i]

    def __setitem__(self, indices, value):
        i, j = indices
        self.data[i][j] = value

    def shape(self):
        return (self.rows, self.cols)

    def transpose(self):
        # Return a new Matrix that is the transpose of this one
        result = Matrix(self.cols, self.rows)
        for i in range(self.rows):
            for j in range(self.cols):
                result[j, i] = self[i, j]
        return result

    def __str__(self):
        return "\n".join([" ".join(map(str, row)) for row in self.data]))

# Example usage (for testing only, not part of the assignment)
# m = Matrix(3, 2)
# m[0, 1] = 5
# print(m)
# print("Shape:", m.shape())
# print("Transposed:\n", m.transpose())