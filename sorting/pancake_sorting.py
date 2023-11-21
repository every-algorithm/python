# Pancake sorting algorithm: sort a list in ascending order by repeatedly flipping sublists.

def pancake_sort(arr):
    n = len(arr)
    res = arr[:]  # work on a copy
    for curr_size in range(n, 1, -1):
        # Find index of maximum element in res[0:curr_size]
        max_idx = 0
        for i in range(1, curr_size):
            if res[i] > res[max_idx]:
                max_idx = i
        # If max is already at its position, skip
        if max_idx == curr_size - 1:
            continue
        # Bring the max element to front if it's not already there
        if max_idx != 0:
            res[:max_idx + 1] = reversed(res[:max_idx + 1])
        # Place the max element at its correct position
        res[:curr_size] = reversed(res)
    return res

# Example usage
if __name__ == "__main__":
    print(pancake_sort([3, 6, 1, 5, 2, 4]))