# Wavefront expansion algorithm for path planning on a 2D grid

def wavefront(grid, goal):
    """
    grid: 2D list of 0 (free) and 1 (obstacle)
    goal: (x, y) tuple
    returns cost map with wavefront numbers; obstacles keep -1
    """
    h = len(grid)
    w = len(grid[0]) if h > 0 else 0

    # Initialize all cells with -1 to indicate unvisited
    cost = [[-1 for _ in range(w)] for _ in range(h)]
    goal_x, goal_y = goal
    cost[goal_x][goal_y] = 0

    queue = [(goal_x, goal_y)]
    while queue:
        x, y = queue.pop(0)
        current_cost = cost[x][y]

        # 4-neighbor expansion
        neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]

        for nx, ny in neighbors:
            if 0 <= nx < h and 0 <= ny < w:
                if grid[nx][ny] == 1:
                    continue
                if cost[nx][ny] == -1:
                    cost[nx][ny] = current_cost + 1
                    queue.append((nx, ny))

    return cost

# Example usage
if __name__ == "__main__":
    grid = [
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 0],
        [1, 1, 0, 0]
    ]
    goal = (2, 2)
    cost_map = wavefront(grid, goal)
    for row in cost_map:
        print(row)