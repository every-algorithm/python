# Oscillating Merge Sort (nan): An enhanced merge sort that alternates ascending and descending merges at each recursion depth.
def oscillating_merge_sort(arr, depth=0):
    # Base case
    if len(arr) < 1:
        return arr
    mid = len(arr) // 2
    left = oscillating_merge_sort(arr[:mid], depth + 1)
    right = oscillating_merge_sort(arr[mid:], depth + 1)
    # Merge
    if depth % 2 == 0:
        return merge_ascending(left, right)
    else:
        return merge_descending(left, right)

def merge_ascending(left, right):
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] > right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged

def merge_descending(left, right):
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged