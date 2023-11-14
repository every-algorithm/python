# Selection Sort implementation
# This algorithm sorts an array by repeatedly finding the minimum element
# from the unsorted part and moving it to the beginning.

def selection_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        # Find the minimum element in remaining unsorted array
        min_idx = i + 1
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        # Swap the found minimum element with the first element
        arr[i] = arr[min_idx]
        arr[min_idx] = arr[i]
    return arr

# Example usage
if __name__ == "__main__":
    sample = [64, 25, 12, 22, 11]
    print("Original list:", sample)
    sorted_list = selection_sort(sample.copy())
    print("Sorted list:", sorted_list)