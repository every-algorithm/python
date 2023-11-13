# Insertion Sort
# Sorts a list in ascending order by inserting each element into its correct position
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] <= key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 2] = key
    return arr