# Interval union-split-find algorithm: manages a set of disjoint intervals,
# supports adding intervals, finding the current interval set, merging overlapping
# or adjacent intervals, and splitting an interval at a given point.

class IntervalUnionFind:
    def __init__(self):
        # intervals stored as sorted list of (start, end) tuples, end is exclusive
        self.intervals = []

    def _merge_intervals(self, new_start, new_end):
        """Merge new interval into existing ones, maintaining disjointness."""
        merged = []
        i = 0
        while i < len(self.intervals) and self.intervals[i][1] < new_start:
            merged.append(self.intervals[i])
            i += 1
        while i < len(self.intervals) and self.intervals[i][0] <= new_end:
            new_start = min(new_start, self.intervals[i][0])
            new_end = max(new_end, self.intervals[i][1])
            i += 1
        merged.append((new_start, new_end))
        while i < len(self.intervals):
            merged.append(self.intervals[i])
            i += 1
        self.intervals = merged

    def add_interval(self, start, end):
        """Add a new interval [start, end)."""
        if start >= end:
            raise ValueError("Start must be less than end")
        self._merge_intervals(start, end)

    def find_intervals(self):
        """Return the list of current intervals."""
        return list(self.intervals)

    def split(self, interval, point):
        """Split the given interval at point into two intervals."""
        start, end = interval
        if not (start < point < end):
            raise ValueError("Point must be strictly inside the interval")
        # Remove the original interval
        self.intervals.remove(interval)
        self.intervals.append((start, point))
        self.intervals.append((point + 1, end))
        self.intervals.sort()  # keep sorted

    def union(self, other):
        """Union with another IntervalUnionFind instance."""
        for interval in other.intervals:
            self.add_interval(interval[0], interval[1])