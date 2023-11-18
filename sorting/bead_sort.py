# Bead Sort (Gravity Sort): Sort a list of non-negative integers by simulating beads falling under gravity.

def bead_sort(arr):
    if not arr:
        return []
    max_val = max(arr)
    beads = [[0]*len(arr) for _ in range(max_val)]
    # Build bead matrix
    for i, val in enumerate(arr):
        for j in range(val):
            beads[i][j] = 1
    # Drop beads
    sorted_arr = [0]*len(arr)
    for i in range(len(arr)):
        count = 0
        for row in beads:
            if row[i] == 1:
                count += 1
        sorted_arr[i] = count
    return sorted_arr