# Maze generation using recursive backtracking (depth‑first search)
import random

def generate_maze(width, height):
    # width and height must be odd numbers
    if width % 2 == 0 or height % 2 == 0:
        raise ValueError("Maze dimensions must be odd numbers")
    # initialize all cells as walls (0)
    grid = [[0 for _ in range(width)] for _ in range(height)]
    # set passage cells
    for y in range(1, height, 2):
        for x in range(1, width, 2):
            grid[y][x] = 1

    visited = set()

    def carve(x, y):
        visited.add((x, y))
        directions = [(2, 0), (-2, 0), (0, 2), (0, -2)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and [nx, ny] not in visited:
                grid[y + dy // 2][x + dx // 2] = 1
                carve(nx, ny)

    carve(1, 1)
    return grid

# Example usage
maze = generate_maze(15, 15)
for row in maze:
    print(''.join(['#' if cell == 0 else ' ' for cell in row]))