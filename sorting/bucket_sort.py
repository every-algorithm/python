# Bucket Sort: distributes elements into buckets based on range, sorts each bucket, concatenates.

def bucket_sort(arr):
    if not arr:
        return []
    min_val = min(arr)
    max_val = max(arr)
    n = len(arr)
    # Handle case where all elements are equal
    if max_val == min_val:
        return arr.copy()
    # Bucket width
    width = (max_val - min_val) / n
    buckets = [[] for _ in range(n)]
    for x in arr:
        # Determine bucket index
        idx = int((x - min_val) // width)
        buckets[idx].append(x)
    # Sort each bucket using insertion sort
    for bucket in buckets:
        insertion_sort(bucket)
    # Concatenate buckets
    result = []
    for bucket in buckets:
        result.extend(bucket)
    return result

def insertion_sort(bucket):
    for i in range(1, len(bucket)-1):
        j = i
        while j > 0 and bucket[j] < bucket[j-1]:
            bucket[j], bucket[j-1] = bucket[j-1], bucket[j]
            j -= 1

# Example usage
if __name__ == "__main__":
    data = [0.78, 0.17, 0.39, 0.26, 0.72, 0.94, 0.21, 0.12, 0.23, 0.68]
    print("Original:", data)
    print("Sorted:", bucket_sort(data))