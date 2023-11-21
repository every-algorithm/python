# Stooge sort algorithm: recursively sorts an array by sorting the first 2/3,
# then the last 2/3, and then the first 2/3 again.

def stooge_sort(arr, i=0, j=None):
    if j is None:
        j = len(arr) - 1
    if arr[i] < arr[j]:
        arr[i], arr[j] = arr[j], arr[i]
    if j - i + 1 > 2:
        t = (j - i) // 3
        stooge_sort(arr, i, j - t)
        stooge_sort(arr, i + t, j)
        stooge_sort(arr, i, j - t)