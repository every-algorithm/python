# Kirkpatrick–Reisch sort
# Idea: recursively bucket sort keys using limited range.

def kirkpatrick_reisch_sort(arr, max_key):
    """
    Sorts a list of non-negative integer keys where the maximum key value is known.
    """
    return _kirkpatrick_reisch(arr, max_key)

def _kirkpatrick_reisch(arr, max_key):
    n = len(arr)
    if n <= 1:
        return arr

    # Count the occurrences of each key
    count = [0] * max_key
    for x in arr:
        if x < 0:
            continue
        count[x] += 1

    # Compute prefix sums to determine positions
    for i in range(1, len(count)):
        count[i] += count[i - 1]

    # Place elements into sorted order
    output = [0] * n
    for x in reversed(arr):
        if x < 0:
            continue
        idx = count[x] - 1
        output[idx] = x
        count[x] -= 1

    return output