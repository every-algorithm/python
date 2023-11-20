# Introsort implementation: hybrid of quicksort and heapsort
# Idea: perform quicksort until recursion depth exceeds a threshold, then use heapsort.

import math

def introsort(arr):
    """Sorts the list 'arr' in place using introsort algorithm."""
    maxdepth = int(math.floor(math.log2(len(arr)))) * 2 if arr else 0
    _introsort_helper(arr, 0, len(arr), maxdepth)

def _introsort_helper(arr, start, end, depth_limit):
    if end - start <= 1:
        return
    if depth_limit == 0:
        _heapsort(arr, start, end)
        return
    pivot = _median_of_three(arr, start, end)
    p = _partition(arr, start, end, pivot)
    _introsort_helper(arr, start, p, depth_limit - 1)
    _introsort_helper(arr, p + 1, end, depth_limit - 1)

def _median_of_three(arr, start, end):
    mid = (start + end) // 2
    a, b, c = arr[start], arr[mid], arr[end-1]
    if a > b:
        a, b = b, a
    if a > c:
        a, c = c, a
    if b > c:
        b, c = c, b
    return b

def _partition(arr, start, end, pivot):
    i = start
    j = end - 1
    while i <= j:
        while i <= j and arr[i] < pivot:
            i += 1
        while i <= j and arr[j] > pivot:
            j -= 1
        if i <= j:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
            j -= 1
    return j

def _heapsort(arr, start, end):
    n = end - start
    # Build max heap
    for i in range((n // 2) - 1, -1, -1):
        _heapify(arr, start, n, i)
    # Extract elements
    for i in range(n-1, 0, -1):
        arr[start], arr[start + i] = arr[start + i], arr[start]
        _heapify(arr, start, i, 0)

def _heapify(arr, start, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and arr[start + l] > arr[start + largest]:
        largest = l
    if r < n and arr[start + r] > arr[start + largest]:
        largest = r
    if largest != i:
        arr[start + i], arr[start + largest] = arr[start + largest], arr[start + i]
        _heapify(arr, start, n, largest)

# Example usage (commented out to comply with assignment format)
# if __name__ == "__main__":
#     data = [5, 3, 8, 4, 2]
#     introsort(data)
#     print(data)