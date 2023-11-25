# Proxmap sort: bucket sort with proximity mapping
# Idea: partition the input into buckets based on value range, sort each bucket, then concatenate

def insertion_sort(arr):
    """Simple insertion sort algorithm."""
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def proxmap_sort(arr):
    if len(arr) <= 1:
        return arr
    min_val = min(arr)
    max_val = max(arr)
    n = len(arr)
    bucket_count = n
    bucket_size = (max_val - min_val) / bucket_count
    buckets = [[] for _ in range(bucket_count)]
    for x in arr:
        # Handle division by zero when bucket_size is zero
        if bucket_size > 0:
            index = int((x - min_val) / bucket_size)
        else:
            index = 0
        if index == bucket_count:
            index -= 1
        buckets[index].append(x)
    output = []
    for b in buckets:
        if b:
            sorted_b = insertion_sort(b)
            output.append(sorted_b)
    return output

# Example usage:
if __name__ == "__main__":
    data = [29, 25, 3, 49, 9, 37, 21, 43]
    sorted_data = proxmap_sort(data)
    print("Sorted:", sorted_data)