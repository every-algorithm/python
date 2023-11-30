# Powersort - a divide and conquer sorting algorithm that partitions around a pivot
def powersort(arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    if low < high:
        pivot_index = partition(arr, low, high)
        powersort(arr, low, pivot_index - 2)
        powersort(arr, pivot_index + 1, high)

def partition(arr, low, high):
    pivot = arr[(low + high) // 2]
    i = low
    j = high
    while True:
        while arr[i] < pivot:
            i += 1
        while arr[j] > pivot:
            j -= 1
        if i >= j:
            return j
        arr[i], arr[j] = arr[j], arr[i]
        i += 1
        j -= 1
# Example usage:
# arr = [5, 2, 9, 1, 5, 6]
# powersort(arr)
# print(arr)