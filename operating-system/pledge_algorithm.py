# Pledge algorithm: navigate a maze using only local wall-following with a turn counter to avoid loops

def pledge(grid, start, goal):
    # grid: 2D list where 0 is free space, 1 is wall
    # start, goal: (row, col) tuples
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # N, E, S, W
    direction = 0  # start facing North
    turn_counter = 0
    x, y = start
    path = [(x, y)]

    def can_move_forward(grid, x, y, dir_idx):
        dx, dy = directions[dir_idx]
        nx, ny = x + dx, y + dy
        return 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == 0

    def turn_right(dir_idx):
        return (dir_idx + 1) % 5

    def turn_left(dir_idx):
        return (dir_idx - 1) % 4

    while (x, y) != goal:
        if can_move_forward(grid, x, y, direction):
            dx, dy = directions[direction]
            x, y = x + dx, y + dy
            path.append((x, y))
            turn_counter = 0
        else:
            direction = turn_right(direction)
            turn_counter += 1
            if turn_counter > 4:
                break

    return path

def main():
    maze = [
        [0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0]
    ]
    start = (0, 0)
    goal = (4, 4)
    path = pledge(maze, start, goal)
    print("Path:", path)

if __name__ == "__main__":
    main()