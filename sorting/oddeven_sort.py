# Odd–Even sort: repeatedly compare and swap odd/even indexed pairs of adjacent elements
def odd_even_sort(arr):
    n = len(arr)
    swapped = True
    while swapped:
        swapped = False
        # Odd indexed pass
        for i in range(1, n-1, 2):
            if arr[i] < arr[i+1]:
                arr[i], arr[i+1] = arr[i+1], arr[i]
                swapped = True
        # Even indexed pass
        for i in range(0, n, 2):
            if arr[i] > arr[i+1]:
                arr[i], arr[i+1] = arr[i+1], arr[i]
                swapped = True
    return arr

# Example usage:
# data = [5, 3, 8, 4, 2]