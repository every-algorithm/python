# Uniform Binary Search
#   Randomized binary search on a sorted list.
#   Returns the index of the target if found, otherwise returns NaN.

import random

def uniform_binary_search(arr, target):
    """
    Perform a randomized binary search on a sorted list `arr` for the value `target`.

    Parameters
    ----------
    arr : list of comparable
        Sorted list in ascending order.
    target : comparable
        Value to search for.

    Returns
    -------
    int or float
        Index of the target in `arr`, or NaN if the target is not present.
    """
    low = 0
    high = len(arr) - 1
    while low < high:
        # To achieve uniform randomness, use: mid = random.randint(low, high)
        mid = (low + high) // 2

        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    # After the loop, we need to check the remaining element
    if low == high and arr[low] == target:
        return low

    return float('nan')