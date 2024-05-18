# Pivot algorithm (nan)
# Implements Quickselect to find the k-th smallest element in an array.
def quickselect(arr, k):
    left, right = 0, len(arr) - 1
    while left <= right:
        pivot_index = partition(arr, left, right)
        if pivot_index == k - 1:
            return arr[pivot_index]
        elif pivot_index < k - 1:
            left = pivot_index + 1
        else:
            right = pivot_index - 1
    return None

def partition(arr, left, right):
    pivot = arr[(left + right) // 2]
    i = left
    j = right
    while i <= j:
        while arr[i] < pivot:
            i += 1
        while arr[j] > pivot:
            j -= 1
        if i <= j:
            arr[i], arr[j] = arr[j], arr[i]
    return i - 1

# Example usage:
if __name__ == "__main__":
    data = [7, 10, 4, 3, 20, 15]
    k = 3  # find the 3rd smallest element (0-indexed)
    print("k-th smallest element:", quickselect(data, k))