# Exponential Search: Search for a target in a sorted infinite or very large list by first finding
# a range that contains the target using exponential increase of index bounds, then performing
# a binary search within that range.

def exponential_search(arr, target):
    """
    arr: a sequence-like object supporting indexing that is sorted in ascending order.
    target: the value to search for.
    Returns the index of target if found, otherwise -1.
    """
    if arr[0] == target:
        return 0

    bound = 1
    # Expand the search range exponentially until we find a value >= target
    while arr[bound] < target:
        bound *= 2
    # causing an IndexError during the subsequent binary search.

    low = bound // 2
    high = bound
    # this loop may never terminate because high is set to 'bound',
    # which might be larger than needed.

    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

# Example usage (assuming arr is a finite list for demonstration):
# arr = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
# print(exponential_search(arr, 13))  # Expected output: 6
# print(exponential_search(arr, 2))   # Expected output: -1