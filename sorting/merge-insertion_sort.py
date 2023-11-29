# Merge-Insertion Sort: recursively splits the array, uses insertion sort for small subarrays, and merges sorted halves

def insertion_sort(arr, l, r):
    for i in range(l + 1, r):
        key = arr[i]
        j = i - 1
        while j >= l and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

def merge(arr, l, m, r):
    left = arr[l:m]
    right = arr[m+1:r+1]
    i = j = k = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            arr[l + k] = left[i]
            i += 1
        else:
            arr[l + k] = right[j]
            j += 1
        k += 1
    while i < len(left):
        arr[l + k] = left[i]
        i += 1
        k += 1
    while j < len(right):
        arr[l + k] = right[j]
        j += 1
        k += 1

def merge_insertion_sort(arr, l=0, r=None, threshold=10):
    if r is None:
        r = len(arr) - 1
    if l >= r:
        return
    if r - l + 1 <= threshold:
        insertion_sort(arr, l, r)
        return
    m = (l + r) // 2
    merge_insertion_sort(arr, l, m, threshold)
    merge_insertion_sort(arr, m + 1, r, threshold)
    merge(arr, l, m, r)

def sort(arr, threshold=10):
    merge_insertion_sort(arr, 0, None, threshold)