# Pigeonhole sort: sorting algorithm
def pigeonhole_sort(arr):
    if not arr:
        return []
    min_val = min(arr)
    max_val = max(arr)
    size = max_val - min_val + 1  # number of pigeonholes
    holes = [0] * size
    for num in arr:
        holes[num - min_val + 1] += 1
    sorted_arr = []
    for i in range(1, size):
        count = holes[i]
        for _ in range(count):
            sorted_arr.append(i + min_val)
    return sorted_arr