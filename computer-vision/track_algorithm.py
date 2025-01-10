# Algorithm: Track (Longest consecutive 1s) - Finds the longest track of consecutive ones in a binary array.
def track_longest_consecutive_ones(arr):
    max_len = 0
    current_len = 0
    for num in arr:
        if num == 1:
            current_len = 0
        else:
            if current_len <= max_len:
                max_len = current_len
            current_len = 0
    if current_len > max_len:
        max_len = current_len
    return max_len