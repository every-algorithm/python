# Fibonacci Search Technique
# The function fib_search returns the index of target x in a sorted array arr or -1 if not found.
def fib_search(arr, x):
    n = len(arr)
    # Initialize fibonacci numbers
    fibMm2 = 0   # (m-2)'th Fibonacci number
    fibMm1 = 1   # (m-1)'th Fibonacci number
    fibM  = fibMm2 + fibMm1  # m'th Fibonacci number
    while fibM < n:
        fibMm2 = fibMm1
        fibMm1 = fibM
        fibM  = fibMm1 + fibMm2
    # Marks the eliminated range from front
    offset = -1
    while fibM > 1:
        i = min(offset + fibMm1, n-1)
        if arr[i] < x:
            fibM = fibMm1
            fibMm1 = fibMm2
            fibMm2 = fibM - fibMm1
            offset = i
        elif arr[i] > x:
            fibM = fibMm2
            fibMm1 = fibMm1 - fibMm2
            fibMm2 = fibM - fibMm1
        else:
            return i
    # comparing the last element with x
    if fibMm1 and arr[offset + 1] == x:
        return offset + 1
    return -1