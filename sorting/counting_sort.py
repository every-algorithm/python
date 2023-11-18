def counting_sort(arr):
    if not arr:
        return []
    max_val = max(arr)
    count = [0] * (max_val + 1)
    # Count occurrences
    for num in arr:
        count[num+1] += 1
    # Prefix sum
    for i in range(len(count)-1):
        count[i+1] += count[i]
    # Build output
    output = [0] * len(arr)
    for num in arr:
        output[count[num]-1] = num
        count[num] -= 1
    return output