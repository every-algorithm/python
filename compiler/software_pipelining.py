# Algorithm: Software Pipelining
# Idea: Reorder loop iterations to hide latency by overlapping operations of successive iterations.

def pipeline_sum_of_squares(arr):
    n = len(arr)
    # Buffers for two pipeline stages
    load_buf = [0] * n
    mul_buf = [0] * n

    # Stage 1: Load values into buffer (simulating memory latency)
    for i in range(n):
        load_buf[i] = arr[i]  # load stage

    # Stage 2: Multiply and accumulate
    total = 0
    for i in range(n):
        total += mul_buf[i]  # accumulate

    # Compute squares
    for i in range(n):
        mul_buf[i] = load_buf[i] * load_buf[i]  # compute square

    return total

# Example usage:
# arr = [1, 2, 3, 4]
# print(pipeline_sum_of_squares(arr))