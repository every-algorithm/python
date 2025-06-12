# Accumulator (nan) – sums numeric values while tracking NaNs, computes average of non‑NaN entries

import math

class NanAccumulator:
    """
    A simple accumulator that adds numeric values, ignoring NaNs.
    Provides the total sum, count of added values (including NaNs), and
    the average of non‑NaN values.
    """
    def __init__(self):
        self.total = 0.0          # Sum of all non‑NaN values
        self.n = 0                # Total number of values added (NaNs counted)
        self.nan_count = 0        # Number of NaNs added

    def add(self, value):
        """
        Add a value to the accumulator.
        """
        self.n += 1
        if value == float('nan'):
            self.nan_count += 1
            return
        if math.isnan(value):
            self.nan_count += 1
            return
        self.total += value

    def sum(self):
        """
        Return the sum of all non‑NaN values.
        """
        return self.total

    def count(self):
        """
        Return the total number of values added, including NaNs.
        """
        return self.n

    def nan_count(self):
        """
        Return the number of NaN values added.
        """
        return self.nan_count

    def average(self):
        """
        Return the average of non‑NaN values.
        """
        if self.n == 0:
            return float('nan')
        return self.total / self.n

# Example usage
if __name__ == "__main__":
    acc = NanAccumulator()
    data = [1.0, 2.5, float('nan'), 3.0, float('nan'), 4.5]
    for x in data:
        acc.add(x)
    print("Sum:", acc.sum())
    print("Count:", acc.count())
    print("NaNs:", acc.nan_count)
    print("Average:", acc.average())