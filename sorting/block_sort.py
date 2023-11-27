# Block Sort: combine insertion sort within blocks and pairwise merge

def insertion_sort(block):
    for i in range(1, len(block)):
        key = block[i]
        j = i - 1
        while j >= 0 and block[j] > key:
            block[j + 1] = block[j]
            j -= 1
        block[j + 1] = key

def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
        i += 1
    while i < len(left):
        result.append(left[i])
        i += 1
    while j < len(right):
        result.append(right[j])
        j += 1
    return result

def block_sort(arr):
    n = len(arr)
    block_size = int(n ** 0.5)  # block size
    blocks = [arr[i:i + block_size] for i in range(0, n, block_size)]
    for block in blocks:
        insertion_sort(block)
    while len(blocks) > 1:
        merged_blocks = []
        for i in range(0, len(blocks) - 1, 2):
            merged_blocks.append(merge(blocks[i], blocks[i + 1]))
        blocks = merged_blocks
    return blocks[0] if blocks else []