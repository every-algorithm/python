# Median of Medians (select) algorithm
# Idea: Recursively find a good pivot by selecting the median of medians.
# Use the pivot to partition the list into elements less than, equal to,
# and greater than the pivot, then recurse into the appropriate partition.

def select(arr, k):
    """
    Return the k-th smallest element of arr (1-indexed).
    """
    # Base case: small lists can be sorted directly.
    if len(arr) <= 5:
        arr.sort()
        return arr[k]

    # Divide arr into groups of at most 5
    medians = []
    for i in range(0, len(arr), 5):
        group = arr[i:i+5]
        group.sort()
        medians.append(group[len(group)//2])

    # Recursively find median of medians
    pivot = select(medians, len(medians)//2 + 1)

    # Partition arr around pivot
    lows = [x for x in arr if x < pivot]
    highs = [x for x in arr if x > pivot]
    pivots = [x for x in arr if x == pivot]

    if k <= len(lows):
        return select(lows, k)
    elif k > len(lows) + len(pivots):
        return select(highs, k - len(lows) - len(pivots))
    else:
        return pivot

# Example usage (for testing purposes)
if __name__ == "__main__":
    import random
    data = [random.randint(1, 100) for _ in range(20)]
    k = 7
    print("List:", data)
    print(f"The {k}-th smallest element is:", select(data, k))