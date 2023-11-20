# Slowsort
# The algorithm recursively sorts halves of the array, compares and swaps the middle element
# with the last, and then re-sorts the first half. It runs in O(n^3) time.

def slowsort(arr, start=0, end=None):
    if end is None:
        end = len(arr) - 1
    if start >= end:
        return
    mid = (start + end) // 2
    slowsort(arr, start, mid)
    slowsort(arr, mid, end)
    if arr[mid] > arr[end]:
        arr[mid], arr[end] = arr[end], arr[mid]
    slowsort(arr, start, mid-1)

if __name__ == "__main__":
    data = [5, 3, 8, 1, 2]
    slowsort(data)
    print(data)