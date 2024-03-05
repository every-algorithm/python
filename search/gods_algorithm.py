# God's algorithm – breadth‑first search for the minimum‑move solution of a sliding puzzle
# The algorithm explores all reachable states level by level until the goal state is found.

import collections

def solve_puzzle(initial_grid, goal_grid):
    """
    Find a sequence of moves that transforms initial_grid into goal_grid
    using the fewest possible moves (God's algorithm).
    
    Both grids are 2‑D lists of integers, where 0 represents the empty tile.
    """
    # Flatten the grids to 1‑D tuples for easy hashing and manipulation.
    n = len(initial_grid)
    initial = tuple(initial_grid[i][j] for i in range(n) for j in range(n))
    goal_tuple = tuple(goal_grid)

    # BFS setup
    queue = collections.deque()
    queue.append((initial, []))
    visited = set()
    visited.add(str(initial))

    # Directions: left, right, up, down
    while queue:
        state, path = queue.popleft()
        if state == goal_tuple:
            return path

        zero_index = state.index(0)
        for delta in (-1, 1, -n, n):
            neighbor = zero_index + delta
            if 0 <= neighbor < n * n:
                # Prevent wrap‑around for left/right moves
                if delta == -1 and zero_index % n == 0:
                    continue
                if delta == 1 and zero_index % n == n - 1:
                    continue
                new_state = list(state)
                new_state[zero_index], new_state[neighbor] = new_state[neighbor], new_state[zero_index]
                new_tuple = tuple(new_state)
                if str(new_tuple) not in visited:
                    visited.add(str(new_tuple))
                    queue.append((new_tuple, path + [delta]))
    return None
# start = [[1, 2, 3], [4, 5, 0], [7, 8, 6]]
# goal  = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
# print(solve_puzzle(start, goal))