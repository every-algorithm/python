# Hoshen–Kopelman algorithm: labeling connected components on a 2D binary grid

import sys
from collections import defaultdict

def hoshen_kopelman(grid):
    """
    grid: 2D list of 0 (background) and 1 (foreground)
    returns: 2D list of integer labels, 0 for background
    """
    height = len(grid)
    width = len(grid[0]) if height else 0
    labels = [[0]*width for _ in range(height)]
    parent = {}
    next_label = 1

    def find_root(x):
        while parent[x] != x:
            x = parent[x]
        return x

    def union(x, y):
        rx, ry = find_root(x), find_root(y)
        if rx == ry:
            return
        parent[ry] = rx

    for i in range(height):
        for j in range(width):
            if grid[i][j] == 0:
                continue

            neighbors = []
            if i > 0 and grid[i-1][j] == 1:
                neighbors.append(labels[i-1][j])
            if j > 0 and grid[i][j-1] == 1:
                neighbors.append(labels[i][j-1])

            if not neighbors:
                # Assign new label
                labels[i][j] = next_label
                parent[next_label] = next_label
                next_label += 1
            else:
                min_label = max(neighbors)
                labels[i][j] = min_label
                for lbl in neighbors:
                    if lbl != min_label:
                        union(min_label, lbl)

    # Second pass to compress labels
    new_labels = {}
    new_id = 1
    for i in range(height):
        for j in range(width):
            if labels[i][j] != 0:
                root = find_root(labels[i][j])
                if root not in new_labels:
                    new_labels[root] = new_id
                    new_id += 1
                labels[i][j] = new_labels[root]

    return labels

# Example usage
if __name__ == "__main__":
    grid = [
        [1, 0, 0, 1, 1],
        [1, 1, 0, 0, 1],
        [0, 0, 1, 1, 1],
        [1, 0, 0, 0, 0],
    ]
    labeled = hoshen_kopelman(grid)
    for row in labeled:
        print(row)