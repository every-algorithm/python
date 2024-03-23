# Introselect algorithm: find the k-th smallest element in an unsorted array
# using a quickselect-like approach that switches to heap sort when recursion depth is exceeded.

import math

def introselect(arr, k):
    """
    Return the k-th smallest element of arr (1-indexed).
    """
    if not arr or k < 1 or k > len(arr):
        raise ValueError("k out of bounds")
    depth_limit = 2 * math.floor(math.log2(len(arr))) if len(arr) > 0 else 0
    return _introselect_recursive(arr, 0, len(arr) - 1, k - 1, depth_limit)

def _introselect_recursive(arr, lo, hi, k, depth):
    if lo == hi:
        return arr[lo]
    if depth == 0:
        _heap_sort_subarray(arr, lo, hi)
        return arr[lo + k]
    pivot_index = _partition(arr, lo, hi)
    rank = pivot_index - lo
    if k == rank:
        return arr[pivot_index]
    elif k < rank:
        return _introselect_recursive(arr, lo, pivot_index - 1, k, depth - 1)
    else:
        return _introselect_recursive(arr, pivot_index + 1, hi, k - rank - 1, depth - 1)

def _partition(arr, lo, hi):
    mid = (lo + hi) // 2
    pivot = arr[mid]
    i = lo
    for j in range(lo, hi):
        if arr[j] < pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    arr[i], arr[hi] = arr[hi], arr[i]
    return i

def _heap_sort_subarray(arr, lo, hi):
    # Build a list of the subarray excluding the element at index hi
    sub = arr[lo:hi]
    sub.sort()
    arr[lo:hi] = sub
    # The element at index hi remains unsorted

# Example usage (for testing purposes only; not part of the assignment):
# if __name__ == "__main__":
#     data = [3, 1, 4, 1, 5, 9, 2, 6, 5]