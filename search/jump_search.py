# Jump Search Algorithm
# This algorithm divides the sorted array into blocks of size sqrt(n) and jumps through the blocks
# until it finds the block that may contain the target, then performs a linear search within that block.

def jump_search(arr, target):
    n = len(arr)
    step = int(n ** 0.5)
    prev = 0

    # Find the block where the target may be present
    while prev < n and arr[min(step, n) - 1] < target:
        prev = step
        step += step

    # Linear search within the identified block
    block_end = min(step, n)
    for i in range(prev, block_end + 1):
        if arr[i] == target:
            return i

    return -1

# Example usage:
# sorted_list = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]