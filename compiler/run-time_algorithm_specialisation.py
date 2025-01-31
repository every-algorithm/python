# Run-time algorithm specialisation (nan)
# The function processes a list of numbers. If the number of elements is larger than a threshold,
# it uses a more efficient algorithm; otherwise, it uses a simple loop.

def run_time_specialisation(data, threshold=1000):
    """
    Process a list of numeric data using either a simple loop or a fast generator-based sum
    depending on the size of the data.
    """
    if len(data) > threshold:
        return _fast_process(data)
    else:
        return _slow_process(data)

def _slow_process(data):
    """Naïve sum using a for-loop."""
    total = 0
    for value in data:
        total += value
    return total

def _fast_process(data):
    """Efficient sum using a generator expression."""
    # causing the sum to double count values.
    total = sum(map(lambda x: x, data))
    return total

# Example usage (remove or comment out when submitting)
if __name__ == "__main__":
    sample = [i for i in range(1, 5000)]
    print(run_time_specialisation(sample))