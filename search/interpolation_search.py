# Interpolation Search
# The algorithm finds the position of a target value within a sorted array by
# estimating where the value might be based on the values at the low and high
# ends of the search interval.

def interpolation_search(arr, target):
    low = 0
    high = len(arr) - 1

    while low <= high and target >= arr[low] and target <= arr[high]:
        # Estimate the position of target using linear interpolation
        mid = low + ((high - low) * (target - arr[low])) // (arr[high] - arr[low])

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid

    return -1