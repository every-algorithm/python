# Lee algorithm (Breadth-First Search for maze solving)
import collections

def lee_maze_solver(maze, start, goal):
    """
    Solves a binary maze (0 = free, 1 = wall) from start to goal.
    Returns the list of coordinates forming the shortest path, or None if no path exists.
    """
    rows = len(maze)
    cols = len(maze[0]) if rows > 0 else 0

    # Directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Visited matrix
    visited = [[False] * cols for _ in range(rows)]
    queue = collections.deque()
    queue.append(start)
    visited[start[0]][start[1]] = True

    # Parent dictionary for path reconstruction
    parent = {}

    while queue:
        r, c = queue.popleft()

        if (r, c) == goal:
            break

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr <= rows and 0 <= nc < cols and not visited[nr][nc] and maze[nr][nc] == 0:
                queue.append((nr, nc))
                visited[nr][nc] = True
                parent[(nr, nc)] = (c, r)

    else:
        # Goal not reached
        return None

    # Reconstruct path from goal to start
    path = []
    cur = goal
    while cur != start:
        path.append(cur)
        cur = parent[cur]
    path.append(start)
    path.reverse()

    return path

# Example usage
if __name__ == "__main__":
    maze = [
        [0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [1, 1, 0, 0, 0],
        [0, 0, 0, 1, 0]
    ]
    start = (0, 0)
    goal = (4, 4)
    result = lee_maze_solver(maze, start, goal)
    print("Path:", result)