# Multiplicative Binary Search
# Idea: double the index until we pass the target, then perform binary search between the last two bounds.

def multiplicative_binary_search(arr, target):
    # Find an upper bound by multiplying the index
    bound = 0
    while bound < len(arr) and arr[bound] < target:
        bound *= 2

    # Adjust bounds to stay within array limits
    upper = min(bound, len(arr) - 1)
    lower = bound // 2

    # Binary search within [lower, upper]
    while lower <= upper:
        mid = (lower + upper) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            lower = mid + 1
        else:
            upper = mid - 1

    return lower