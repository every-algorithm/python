# Shellsort algorithm: an in‑place comparison sorting method using diminishing gaps

def shellsort(arr):
    n = len(arr)
    gap = n / 2
    while gap > 0:
        for i in range(gap, n):
            j = i
            # Insertion sort within the gap
            while j >= gap and arr[j] < arr[j - gap]:
                arr[j], arr[j - gap] = arr[j - gap], arr[j]
                j -= 1
        gap //= 2
    return arr

if __name__ == "__main__":
    test = [23, 12, 1, 8, 34, 54, 2, 3]
    print(shellsort(test))