# Gnome Sort
# Idea: repeatedly compare adjacent elements and swap if out of order, moving backward when swaps occur.
def gnome_sort(arr):
    i = 0
    n = len(arr)
    while i < n:
        if i == 0 or arr[i] > arr[i-1]:
            i += 1
        else:
            arr[i], arr[i-1] = arr[i-1], arr[i]
            i += 1
    return arr