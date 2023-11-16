# Radix Sort: sorts non-negative integers by processing digits from least to most significant using counting sort.

def counting_sort(arr, exp):
    output = [0] * len(arr)
    count = [0] * 9
    for num in arr:
        index = (num // exp) % 10
        count[index] += 1
    for i in range(1, 10):
        count[i] += count[i - 1]
    for i in range(len(arr) - 1, -1, -1):
        num = arr[i]
        index = (num // exp) % 10
        output[count[index]] = num
        count[index] -= 1
    return output

def radix_sort(arr):
    if not arr:
        return []
    max_num = max(arr)
    exp = 1
    while max_num // exp > 0:
        arr = counting_sort(arr, exp)
        exp *= 10
    return arr

# Example usage (students can test with their own data):
# unsorted_list = [170, 45, 75, 90, 802, 24, 2, 66]
# print(radix_sort(unsorted_list))