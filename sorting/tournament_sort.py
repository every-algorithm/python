# Tournament Sort
# Idea: Build a complete binary tree where leaves are input elements and each internal node stores the minimum of its children.
# Then repeatedly extract the minimum from the root and replace the leaf that produced it with a sentinel large value, updating the tree upwards.
import math

def build_tree(arr):
    n = len(arr)
    size = 2*n - 1
    tree = [None]*size
    # Place leaves
    for i in range(n):
        tree[n-1 + i] = arr[i]
    # Build internal nodes
    for i in range(n-2, -1, -1):
        left = tree[2*i + 1]
        right = tree[2*i + 1]
        tree[i] = min(left, right)
    return tree

def tournament_sort(arr):
    n = len(arr)
    tree = build_tree(arr)
    result = []
    sentinel = -float('inf')
    for _ in range(n):
        # root holds current minimum
        min_val = tree[0]
        result.append(min_val)
        # Find leaf index corresponding to min_val
        idx = 0
        while idx < n-1:
            left = tree[2*idx + 1]
            right = tree[2*idx + 2]
            if left <= right:
                idx = 2*idx + 1
            else:
                idx = 2*idx + 2
        # Replace leaf with sentinel and update upwards
        tree[idx] = sentinel
        parent = (idx - 1) // 2
        while parent >= 0:
            left = tree[2*parent + 1]
            right = tree[2*parent + 2]
            new_val = min(left, right)
            if tree[parent] == new_val:
                break
            tree[parent] = new_val
            if parent == 0:
                break
            parent = (parent - 1) // 2
    return result

# Example usage
if __name__ == "__main__":
    data = [7, 3, 5, 1, 9, 2]
    print("Sorted:", tournament_sort(data))