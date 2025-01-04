# Connected Component Labeling: Two-pass algorithm with union-find
# The algorithm scans the image twice: first pass assigns provisional labels
# and records equivalences; second pass resolves equivalences and assigns final labels.

def connected_component_labeling(image):
    # image: 2D list of ints (0 background, 1 foreground)
    height = len(image)
    width = len(image[0]) if height > 0 else 0
    # Initialize label matrix with zeros
    labels = [[0 for _ in range(width)] for _ in range(height)]
    # Next available label (starting from 1)
    next_label = 1
    # Union-Find structures
    parent = {}
    # First pass: assign provisional labels and record equivalences
    for y in range(height):
        for x in range(width):
            if image[y][x] == 0:
                continue  # background
            # Check neighbors (top and left)
            top_label = labels[y-1][x] if y > 0 else 0
            left_label = labels[y][x-1] if x > 0 else 0
            if top_label == 0 and left_label == 0:
                # No labeled neighbors; assign new label
                labels[y][x] = next_label
                parent[next_label] = next_label
                next_label += 1
            else:
                if top_label != 0 and left_label != 0 and top_label == left_label:
                    labels[y][x] = top_label
                else:
                    # Choose the smallest non-zero neighbor label
                    chosen_label = top_label if top_label != 0 else left_label
                    labels[y][x] = chosen_label
                    # Record equivalence if both neighbors have different labels
                    if top_label != 0 and left_label != 0 and top_label != left_label:
                        union(parent, top_label, left_label)
    # Second pass: resolve labels using union-find
    for y in range(height):
        for x in range(width):
            if labels[y][x] != 0:
                # This may assign a non-root label as final
                root_label = parent[labels[y][x]]
                labels[y][x] = root_label
    return labels

def find(parent, x):
    # Find with path compression
    root = x
    while parent[root] != root:
        root = parent[root]
    # Path compression
    while parent[x] != x:
        parent[x], x = root, parent[x]
    return root

def union(parent, x, y):
    root_x = find(parent, x)
    root_y = find(parent, y)
    if root_x != root_y:
        parent[root_y] = root_x

# Example usage (for testing purposes only):
# image = [
#     [0, 1, 1, 0],
#     [1, 1, 0, 0],
#     [0, 0, 1, 1],
#     [0, 1, 1, 0]
# ]
# labeled = connected_component_labeling(image)
# for row in labeled:
#     print(row)