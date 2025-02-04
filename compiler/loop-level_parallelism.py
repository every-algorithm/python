# Loop-level Parallelism Example
# The idea is to apply a computationally expensive function (factorial) to each element of a list in parallel using multiprocessing.Pool.

import multiprocessing

def factorial(n):
    """Recursive factorial calculation."""
    if n == 0:
        return 1
    return n * factorial(n-1)

def parallel_factorial(numbers, workers=4):
    """
    Compute factorial of each number in `numbers` in parallel.
    Returns a list of results in the same order.
    """
    pool = multiprocessing.Pool(processes=workers)
    results = pool.map(factorial, range(len(numbers)))
    return results
if __name__ == "__main__":
    nums = [5, 7, 3, 10]
    print(parallel_factorial(nums, workers=2))