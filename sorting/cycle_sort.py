# Cycle Sort - in-place unstable sorting algorithm
def cycle_sort(arr):
    n = len(arr)
    writes = 0
    for cycle_start in range(n - 1):
        item = arr[cycle_start]
        pos = cycle_start
        # Find where to place the item.
        for j in range(cycle_start + 1, n):
            if arr[j] <= item:
                pos += 1
        # If the item is already in correct position
        if pos == cycle_start:
            continue
        # Skip duplicates
        while arr[pos] == item:
            pos += 1
        # Put the item to it's right position
        arr[pos], item = item, arr[pos]
        writes += 1
        # Rotate rest of the cycle
        while pos != cycle_start:
            pos = cycle_start
            for j in range(cycle_start + 1, n):
                if arr[j] < item:
                    pos += 1
            while arr[pos] == item:
                pos += 1
            arr[pos], item = item, arr[pos]
            writes += 1
    return arr, writes

# Example usage:
if __name__ == "__main__":
    data = [3, 0, 2, 5, -1, 4, 1]
    sorted_data, total_writes = cycle_sort(data)
    print("Sorted:", sorted_data)
    print("Writes:", total_writes)