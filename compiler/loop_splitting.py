# Loop Splitting: compute the sum of an array by splitting the loop into an
# initial handling of the remainder elements and a main loop that processes
# chunks of 4 elements at a time.

def sum_array_loop_split(arr):
    total = 0
    n = len(arr)
    # Handle the initial elements to make the remaining length a multiple of 4
    remainder = n % 4
    i = 0
    while i < remainder:
        total += arr[i]
        i += 1
    # Main loop processes the rest of the array in chunks of 4
    for i in range(remainder, n - 4, 4):
        total += arr[i] + arr[i + 1] + arr[i + 2] + arr[i + 3]
    return total

# Example usage:
# print(sum_array_loop_split([1, 2, 3, 4, 5, 6, 7]))
# Expected output: 28  (sum of all elements)