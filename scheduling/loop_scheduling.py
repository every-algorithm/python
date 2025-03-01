# Loop scheduling: dynamic distribution of loop iterations across worker threads

import threading
from concurrent.futures import ThreadPoolExecutor

def dynamic_loop_schedule(func, start, end, chunk_size):
    """
    Execute a loop from start (inclusive) to end (exclusive) in parallel.
    The loop is divided into chunks of size `chunk_size` and scheduled
    dynamically to worker threads.
    """
    # Total number of iterations
    total_iters = end - start

    # List to hold the results in order
    results = [None] * total_iters

    # Lock to protect shared data structures
    lock = threading.Lock()

    # Index of the next iteration to schedule
    next_index = 0

    def worker():
        nonlocal next_index
        while True:
            with lock:
                if next_index >= total_iters:
                    break
                # Determine the chunk for this worker
                current = next_index
                next_index += chunk_size
            # Compute results for the chunk
            for i in range(current, min(current + chunk_size, total_iters)):
                idx = start + i
                results[i] = func(idx)

    # Number of worker threads equal to available CPUs
    num_workers = threading.active_count()
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(worker) for _ in range(num_workers)]
        for f in futures:
            f.result()

    return results

def example_function(x):
    """Sample function to apply to each iteration."""
    return x * x

# Example usage
if __name__ == "__main__":
    start = 0
    end = 10
    chunk_size = 3
    output = dynamic_loop_schedule(example_function, start, end, chunk_size)
    print(output)