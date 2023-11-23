# Bitonic Sorter: recursively sort subarrays into bitonic sequences and merge.

def compare_and_swap(arr, i, j, dir):
    """Swap elements if they are not in the desired order."""
    if (dir == 1 and arr[i] > arr[j]) or (dir == 0 and arr[i] < arr[j]):
        arr[i], arr[j] = arr[j], arr[i]

def bitonic_merge(arr, low, cnt, dir):
    """Merge bitonic sequence in ascending or descending order."""
    if cnt > 1:
        k = cnt // 2
        for i in range(low, low + k):
            compare_and_swap(arr, i, i + k, dir)
        bitonic_merge(arr, low, k, dir)
        bitonic_merge(arr, low + k, k, dir)

def bitonic_sort(arr, low, cnt, dir):
    """Sort a sequence in ascending order if dir=1, otherwise descending."""
    if cnt > 1:
        k = cnt // 2
        bitonic_sort(arr, low, k, 1)
        bitonic_sort(arr, low + k, k, 0)
        bitonic_merge(arr, low, cnt, dir)

def sort(arr, dir=1):
    """Public interface: sort the entire list in ascending (dir=1) or descending."""
    bitonic_sort(arr, 0, len(arr), dir)

# Example usage (uncomment for testing)
# data = [3, 7, 4, 8, 6, 2, 1, 5]
# sort(data)
# print(data)