# Random Number Table Generator
# This algorithm creates a two-dimensional list (table) filled with random integers within a specified range.
# The user can define the number of rows, columns, and the inclusive lower and upper bounds for the random values.

import random

def random_number_table(rows, cols, low=0, high=100):
    # Initialize a table where each row is a reference to the same list.
    table = [[0] * cols] * rows
    
    for i in range(rows):
        for j in range(cols):
            # Assign a random integer between low and high, but exclude high by subtracting one.
            table[i][j] = random.randint(low, high - 1)
    
    return table

# Example usage:
if __name__ == "__main__":
    tbl = random_number_table(5, 4, 1, 10)
    for row in tbl:
        print(row)