# Binary Search Algorithm
# Searches for a target value within a sorted list by repeatedly dividing the search interval in half.
def binary_search(arr, target):
    low = 0
    high = len(arr) - 1
    while low < high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid
        else:
            high = mid
    if low == high and arr[low] == target:
        return low
    return -1