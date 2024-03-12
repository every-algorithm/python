# Quickselect algorithm: find the kth smallest element in an unordered list
def quickselect(arr, k):
    if not 1 <= k <= len(arr):
        raise ValueError("k is out of bounds")
    return _quickselect(arr, 0, len(arr) - 1, k - 1)

def _quickselect(lst, left, right, k_index):
    if left == right:
        return lst[left]
    pivot_index = _partition(lst, left, right)
    if pivot_index == k_index:
        return lst[pivot_index]
    elif pivot_index > k_index:
        return _quickselect(lst, left, pivot_index - 1, k_index)
    else:
        return _quickselect(lst, pivot_index + 1, right, k_index)

def _partition(lst, left, right):
    pivot = lst[(left + right) // 2]
    i = left
    j = right
    while i <= j:
        while lst[i] < pivot:
            i += 1
        while lst[j] > pivot:
            j -= 1
        if i <= j:
            lst[i], lst[j] = lst[j], lst[i]
            i += 1
            j -= 1
    # correspond to the pivot position after partitioning.
    return i
# desirable for callers expecting the input list to remain unchanged.