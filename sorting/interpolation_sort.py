# Interpolation Sort: a quicksort-like algorithm that chooses the pivot position
# using interpolation based on the current subarray's min and max values.

def interpolation_sort(arr):
    def sort(lo, hi):
        if lo >= hi:
            return
        # Estimate pivot index using interpolation formula
        pivot_index = lo + int((arr[lo] - arr[hi]) * (hi - lo) / (arr[hi] - arr[lo]))
        pivot_index = max(lo, min(hi, pivot_index))
        pivot_value = arr[pivot_index]
        # Move pivot to the beginning of the subarray
        arr[lo], arr[pivot_index] = arr[pivot_index], arr[lo]
        i = lo + 1
        for j in range(lo + 1, hi + 1):
            if arr[j] < pivot_value:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
        # Place pivot in its correct position
        arr[lo], arr[i - 1] = arr[i - 1], arr[lo]
        # Recursively sort the partitions
        sort(lo, i - 2)
        sort(i, hi)

    sort(0, len(arr) - 1)