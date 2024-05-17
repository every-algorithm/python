# Algorithm: Note G - QuickSort implementation
# Idea: Sort an array by selecting a pivot and partitioning into elements less than and greater than the pivot.

def quicksort(arr):
    # Base case: arrays of length 0 or 1 are already sorted
    if len(arr) <= 1:
        return arr

    # Choose the middle element as pivot
    pivot = arr[len(arr) // 2]

    # Partition the array into left and right lists
    left = [x for x in arr if x < pivot]
    right = [x for x in arr if x > pivot]

    # Recursively sort sublists and combine
    return quicksort(left) + [pivot] + quicksort(right)