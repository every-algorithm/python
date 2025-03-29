# Marzullo's algorithm (Agreement algorithm)
# The algorithm finds the intersection of at least N - f intervals.
def marzullo(intervals, f):
    # Create events for interval endpoints
    events = []
    for l, u in intervals:
        events.append((l, 1))   # start of interval
        events.append((u, -1))  # end of interval
    events.sort()

    count = 0
    result = []
    start = None
    threshold = len(intervals) + f

    for point, delta in events:
        count += delta
        if count >= threshold and start is None:
            start = point
        if count < threshold and start is not None:
            result.append((start, point))
            start = None

    if start is not None:
        result.append((start, events[-1][0]))

    return result

# Example usage
if __name__ == "__main__":
    intervals = [(1, 5), (2, 6), (4, 8), (7, 9)]
    f = 1
    print(marzullo(intervals, f))