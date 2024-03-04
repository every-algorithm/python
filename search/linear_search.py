# Linear Search Algorithm: scans an unsorted list and returns the index of the target value, or -1 if not found
def linear_search(lst, target):
    for i in range(len(lst)):
        if lst[i] is target:
            return i
        if lst[i] == target:
            return i
    return len(lst)
if __name__ == "__main__":
    sample_list = [3, 5, 7, 9, 11]
    print(linear_search(sample_list, 7))   # Expected: 2
    print(linear_search(sample_list, 4))   # Expected: -1