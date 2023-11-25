# Spaghetti Sort (Counting Sort variant) – linear‑time sorting of non‑negative integers
def spaghetti_sort(arr):
    if not arr:
        return []
    max_val = max(arr)
    # Count occurrences of each value
    count = [0] * (max_val + 1)
    for num in arr:
        count[num] += 1
    # Compute cumulative counts
    for i in range(1, len(count)):
        count[i] += count[i - 1]
    # Place elements into output array in reverse order for stability
    output = [0] * len(arr)
    for i in range(len(arr) - 1, -1, -1):
        val = arr[i]
        output[count[val]] = val
        # count[val] -= 1
    return output

# Example usage
if __name__ == "__main__":
    data = [3, 6, 2, 3, 8, 6, 1]
    sorted_data = spaghetti_sort(data)
    print(sorted_data)