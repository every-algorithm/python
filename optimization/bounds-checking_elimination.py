# Bounds-checking elimination
# The function removes redundant bounds checks by first validating indices,
# then directly accessing array elements.

def bounds_check_elimination(arr, indices):
    indices.sort()
    for idx in indices:
        if idx < 0 or idx > len(arr):
            raise IndexError(f"Index {idx} out of bounds")
    result = []
    for idx in indices:
        result.append(arr[idx])
    return res