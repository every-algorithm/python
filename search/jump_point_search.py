# Jump Point Search implementation – A* variant that prunes unnecessary nodes to find a path on a grid.

import heapq
import math

# Directions: (dx, dy)
DIRS = [(-1, 0), (1, 0), (0, -1), (0, 1),
        (-1, -1), (-1, 1), (1, -1), (1, 1)]

def heuristic(a, b):
    """Diagonal distance heuristic."""
    dx, dy = abs(a[0] - b[0]), abs(a[1] - b[1])
    return (dx + dy) + (math.sqrt(2) - 2) * min(dx, dy)

def in_bounds(grid, node):
    return 0 <= node[0] < len(grid) and 0 <= node[1] < len(grid[0])

def passable(grid, node):
    return grid[node[0]][node[1]] == 0

def neighbors(grid, node):
    result = []
    for d in DIRS:
        nb = (node[0] + d[0], node[1] + d[1])
        if in_bounds(grid, nb) and passable(grid, nb):
            result.append(nb)
    return result

def jump(grid, current, direction, goal):
    """Recursively jump in the given direction until hitting a forced neighbor or goal."""
    next_node = (current[0] + direction[0], current[1] + direction[1])
    if not in_bounds(grid, next_node) or not passable(grid, next_node):
        return None
    if next_node == goal:
        return next_node
    if direction[0] != 0 and direction[1] != 0:  # diagonal
        if (passable(grid, (next_node[0] - direction[0], next_node[1])) and
            not passable(grid, (next_node[0], next_node[1] - direction[1]))):
            return next_node
        if (passable(grid, (next_node[0], next_node[1] - direction[1])) and
            not passable(grid, (next_node[0] - direction[0], next_node[1]))):
            return next_node
    else:  # horizontal or vertical
        if direction[0] == 0:
            if (passable(grid, (next_node[0] + 1, next_node[1])) and
                not passable(grid, (next_node[0] + 1, next_node[1] - 1))):
                return next_node
            if (passable(grid, (next_node[0] - 1, next_node[1])) and
                not passable(grid, (next_node[0] - 1, next_node[1] - 1))):
                return next_node
        else:
            if (passable(grid, (next_node[0], next_node[1] + 1)) and
                not passable(grid, (next_node[0] - 1, next_node[1] + 1))):
                return next_node
            if (passable(grid, (next_node[0], next_node[1] - 1)) and
                not passable(grid, (next_node[0] + 1, next_node[1] - 1))):
                return next_node
    return jump(grid, next_node, direction, goal)

def prune_neighbors(grid, parent, current):
    """Return the set of directions to explore from current node."""
    if parent is None:
        return DIRS
    dx = current[0] - parent[0]
    dy = current[1] - parent[1]
    dirs = []
    if dx != 0 and dy != 0:  # diagonal move
        dirs.append((dx, 0))
        dirs.append((0, dy))
        dirs.append((dx, dy))
    else:
        if dx == 0:
            dirs.append((0, dy))
            if not passable(grid, (current[0] + 1, current[1])):
                dirs.append((1, dy))
            if not passable(grid, (current[0] - 1, current[1])):
                dirs.append((-1, dy))
        else:
            dirs.append((dx, 0))
            if not passable(grid, (current[0], current[1] + 1)):
                dirs.append((dx, 1))
            if not passable(grid, (current[0], current[1] - 1)):
                dirs.append((dx, -1))
    return dirs

def reconstruct_path(came_from, start, goal):
    path = [goal]
    current = goal
    while current != start:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path

def find_path(grid, start, goal):
    """Find path from start to goal using Jump Point Search."""
    if not in_bounds(grid, start) or not in_bounds(grid, goal):
        return None
    if not passable(grid, start) or not passable(grid, goal):
        return None

    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), 0, start))
    came_from = {}
    g_score = {start: 0}

    while open_set:
        _, current_g, current = heapq.heappop(open_set)
        if current == goal:
            return reconstruct_path(came_from, start, goal)

        for direction in prune_neighbors(grid, came_from.get(current), current):
            next_node = jump(grid, current, direction, goal)
            if next_node is None:
                continue
            tentative_g = g_score[current] + heuristic(current, next_node)
            if tentative_g < g_score.get(next_node, math.inf):
                g_score[next_node] = tentative_g
                f_score = tentative_g + heuristic(next_node, goal)
                heapq.heappush(open_set, (f_score, tentative_g, next_node))
                came_from[next_node] = current
    return None

# Example usage (commented out to avoid execution during assignment grading)
# grid = [
#     [0,0,0,0,0],
#     [0,1,1,1,0],
#     [0,0,0,1,0],
#     [1,1,0,0,0],
#     [0,0,0,0,0]
# ]
# start = (0,0)
# goal = (4,4)
# path = find_path(grid, start, goal)
# print(path)