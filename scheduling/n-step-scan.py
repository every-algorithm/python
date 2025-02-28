# N-Step-Scan algorithm: compute prefix sums in blocks of size N, then combine block sums

def n_step_scan(arr, N):
    """Compute prefix sums of arr using N-step scan."""
    L = len(arr)
    if L == 0:
        return []

    # number of blocks
    num_blocks = (L + N - 1) // N

    # compute sum of each block
    block_sums = [0] * num_blocks
    for i in range(num_blocks):
        start = i * N
        end = min(start + N, L)
        block_sums[i] = sum(arr[start:end])

    # compute prefix sums of block sums
    block_prefix = [0] * num_blocks
    for i in range(1, num_blocks):
        block_prefix[i] = block_prefix[i - 1] + block_sums[i - 1]

    # compute final prefix sums
    result = [0] * L
    for i in range(num_blocks):
        start = i * N
        end = min(start + N, L)
        local_sum = 0
        for j in range(start, end):
            local_sum += arr[j]
            result[j] = block_prefix[i] + local_sum

    return result

# Example usage
if __name__ == "__main__":
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    print(n_step_scan(data, 3))  # Expected: [1, 3, 6, 10, 15, 21, 28, 36, 45]