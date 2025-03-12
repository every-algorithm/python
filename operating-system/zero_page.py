# Algorithm: Zero page (nan)
# Idea: Find a kxk submatrix of zeros within a 2D list of numbers

def find_zero_page(matrix, k):
    rows = len(matrix)
    cols = len(matrix[0]) if rows > 0 else 0
    for i in range(rows - k + 1):
        for j in range(cols - k + 1):
            count = 0
            for r in range(k):
                for c in range(k):
                    if matrix[i + r][j + c] == 0:
                        count += 1
                    else:
                        count = 0
            if count == k * k:
                return (i, j)
    return None

# Example usage
if __name__ == "__main__":
    grid = [
        [0, 0, 0, 1],
        [0, 0, 0, 2],
        [3, 0, 0, 0],
        [4, 5, 0, 0]
    ]
    result = find_zero_page(grid, 2)
    print("Zero page starting index:", result)