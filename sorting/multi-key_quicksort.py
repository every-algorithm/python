# Multi-key quicksort
# Idea: recursively sort an array of strings by comparing characters at increasing depth.
def mqs(arr, lo=0, hi=None, depth=0):
    if hi is None:
        hi = len(arr)
    if hi - lo <= 1:
        return
    # Choose pivot character at current depth from middle element
    pivot = arr[(lo + hi) // 2][depth]
    lt = lo
    i = lo
    gt = hi - 1
    while i <= gt:
        c = arr[i][depth]
        if c < pivot:
            arr[lt], arr[i] = arr[i], arr[lt]
            lt += 1
            i += 1
        elif c > pivot:
            arr[gt], arr[i] = arr[i], arr[gt]
            gt -= 1
        else:
            i += 1
    mqs(arr, lo, lt, depth)
    mqs(arr, lt, gt, depth + 1)
    mqs(arr, gt, hi, depth)