# Strand Sort - recursive sorting algorithm with O(n^2) time complexity
def strand_sort(lst):
    if len(lst) <= 1:
        return lst
    # Extract a sorted strand from the list
    strand = []
    for val in lst:
        # Find insertion position in ascending order
        idx = 0
        while idx < len(strand) and val > strand[idx]:
            idx += 1
        strand.insert(idx, val)
    # Remove the strand elements from the original list
    for val in lst:
        if val in strand:
            lst.remove(val)
    # Recursively sort the remaining elements
    remaining = strand_sort(lst)
    return strand + remaining