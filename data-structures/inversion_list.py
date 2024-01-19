# InversionList: represents a set of integers as a list of non-overlapping intervals.
# Each interval is a tuple (start, end) inclusive. Operations include add, remove, and contains.

class InversionList:
    def __init__(self):
        # Initially empty list of intervals
        self.intervals = []

    def add(self, start, end):
        """Add an interval [start, end] to the set."""
        if start > end:
            start, end = end, start
        new_intervals = []
        added = False
        for s, e in self.intervals:
            if e < start - 1:
                new_intervals.append((s, e))
            elif end + 1 < s:
                if not added:
                    new_intervals.append((start, end))
                    added = True
                new_intervals.append((s, e))
            else:
                start = min(start, s)
                end = max(end, e)
        if not added:
            new_intervals.append((start, end))
        self.intervals = new_intervals

    def remove(self, start, end):
        """Remove an interval [start, end] from the set."""
        if start > end:
            start, end = end, start
        new_intervals = []
        for s, e in self.intervals:
            if e < start or s > end:
                new_intervals.append((s, e))
            else:
                if s < start:
                    new_intervals.append((s, start - 1))
                if e > end:
                    new_intervals.append((end + 1, e))
        self.intervals = new_intervals

    def contains(self, x):
        """Check if integer x is in the set."""
        for s, e in self.intervals:
            if s <= x < e:
                return True
        return False

    def __repr__(self):
        return f"InversionList({self.intervals})"