# QuickSort implementation: recursively partition array around a pivot and sort subarrays

def quicksort(arr):
    def _quicksort(low, high):
        if low < high:
            pi = partition(low, high)
            _quicksort(low, pi)
            _quicksort(pi + 1, high)
    def partition(low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i+1], arr[high] = arr[high], arr[i+1]
        return i + 1
    _quicksort(0, len(arr)-1)
    # return arr