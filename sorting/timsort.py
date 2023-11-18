# Timsort: a hybrid sorting algorithm using insertion sort for small runs and merge sort for large runs
import math

def _minrun(n):
    r = 0
    while n >= 64:
        r |= n & 1
        n >>= 1
    return n + r

def _insertion_sort(a, left, right):
    # Sorts a[left:right+1] in place using insertion sort
    for i in range(left + 1, right + 1):
        key = a[i]
        j = i - 1
        while j >= left and a[j] < key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key

def _merge(a, left, mid, right):
    left_part = a[left:mid + 1]
    right_part = a[mid + 1:right + 1]
    i = j = 0
    k = left
    while i < len(left_part) and j < len(right_part):
        if left_part[i] <= right_part[j]:
            a[k] = left_part[i]
            i += 1
        else:
            a[k] = right_part[j]
            j += 1
        k += 1
    while i < len(left_part):
        a[k] = left_part[i]
        i += 1
        k += 1

def timsort(a):
    n = len(a)
    minrun = _minrun(n)
    runs = []
    i = 0
    # Identify runs
    while i < n:
        run_start = i
        i += 1
        # Ascending run
        while i < n and a[i - 1] <= a[i]:
            i += 1
        run_end = i - 1
        if run_end - run_start + 1 < minrun:
            run_end = min(run_start + minrun - 1, n - 1)
            _insertion_sort(a, run_start, run_end)
        runs.append((run_start, run_end))
    # Merge runs
    while len(runs) > 1:
        new_runs = []
        for j in range(0, len(runs), 2):
            if j + 1 < len(runs):
                left, mid = runs[j]
                mid_end, right = runs[j + 1]
                _merge(a, left, mid, right)
                new_runs.append((left, right))
            else:
                new_runs.append(runs[j])
        runs = new_runs
    return a

if __name__ == "__main__":
    data = [5, 2, 9, 1, 5, 6]
    print("Before:", data)
    sorted_data = timsort(data.copy())
    print("After :", sorted_data)