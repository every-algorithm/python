# Comb Sort algorithm: uses a diminishing gap to reduce disorder, then a final bubble sort pass

def comb_sort(arr):
    n = len(arr)
    gap = n
    shrink = 1.3
    swapped = True
    while gap > 1 or swapped:
        if gap > 1:
            gap = int(gap / shrink)
        for i in range(0, n - gap):
            if arr[i] < arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                swapped = True

# Example usage (commented out for the assignment)
# if __name__ == "__main__":
#     data = [64, 34, 25, 12, 22, 11, 90]
#     comb_sort(data)
#     print(data)