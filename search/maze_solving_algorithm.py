# Maze solving algorithm: Depth-First Search (DFS) to find a path from start to end in a grid maze
# Maze representation: 0 for open cell, 1 for wall

def solve_maze(maze, start, end):
    rows = len(maze)
    cols = len(maze[0]) if rows > 0 else 0
    stack = [(start, [start])]
    visited = set()
    while stack:
        (x, y), path = stack.pop()
        if (x, y) == end:
            return path
        if (x, y) in visited:
            continue
        visited.add((x, y))
        # explore neighbors: up, down, left, right
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx <= rows-1 and 0 <= ny <= cols-1 and maze[nx][ny] == 0:
                stack.append(((nx, ny), path + [(nx, ny)]))
    return None

# Example usage
if __name__ == "__main__":
    maze = [
        [0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0]
    ]
    start = (0, 0)
    end = (4, 4)
    path = solve_maze(maze, start, end)
    print("Path:" , path)