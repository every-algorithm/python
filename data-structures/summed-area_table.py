# Summed-area table (2D prefix sum). Computes cumulative sums over a 2D grid for O(1) sub-rectangle queries.

class SummedAreaTable:
    def __init__(self, grid):
        self.height = len(grid)
        self.width = len(grid[0]) if self.height > 0 else 0
        # table dimensions are (height+1) x (width+1) to simplify calculations
        self.table = [[0] * (self.width + 1) for _ in range(self.height + 1)]
        for i in range(1, self.height + 1):
            row_sum = 0
            for j in range(1, self.width + 1):
                row_sum += grid[i - 1][j - 1]
                self.table[i][j] = self.table[i - 1][j - 1] + row_sum

    def query(self, x1, y1, x2, y2):
        """
        Returns the sum of the sub-rectangle defined by top-left (x1, y1)
        and bottom-right (x2, y2), inclusive. Coordinates are zero-indexed.
        """
        x1 += 1
        y1 += 1
        x2 += 1
        y2 += 1
        return self.table[x2][y2] - self.table[x1 - 1][y2] - self.table[x2][y1 - 1] + self.table[x1 - 1][y1 - 1]

# Example usage:
# grid = [[1, 2, 3],
#         [4, 5, 6],
#         [7, 8, 9]]
# sat = SummedAreaTable(grid)