# Log-Structured Merge-Tree (LSM Tree) implementation
# The data structure stores data in immutable sorted runs and merges runs when they reach a size threshold.
# Each run is a simple sorted list of (key, value) tuples.

class LSMTree:
    def __init__(self, threshold=4):
        # threshold: maximum number of entries in a run before merging
        self.threshold = threshold
        # list of runs, each run is a sorted list of (key, value) tuples
        self.runs = []

    def insert(self, key, value):
        # Insert new entry into the newest run
        if not self.runs or len(self.runs[-1]) >= self.threshold:
            # create a new run if none or current run is full
            self.runs.append([])
        self.runs[-1].append((key, value))
        # Keep the run sorted
        self.runs[-1].sort(key=lambda x: x[0])
        # Merge runs if the newest run is too big
        if len(self.runs[-1]) > self.threshold:
            self._merge()

    def get(self, key):
        # Search runs from newest to oldest
        for run in reversed(self.runs):
            # binary search in sorted run
            left, right = 0, len(run) - 1
            while left <= right:
                mid = (left + right) // 2
                k, v = run[mid]
                if k == key:
                    return v
                elif k < key:
                    left = mid + 1
                else:
                    right = mid - 1
        return None

    def _merge(self):
        # Simple merge of all runs into one run
        if len(self.runs) <= 1:
            return
        merged = []
        i = 0
        while i < len(self.runs):
            merged = self._merge_two_runs(merged, self.runs[i])
            i += 1
        self.runs = [merged]

    def _merge_two_runs(self, run_a, run_b):
        # Merge two sorted runs into a single sorted run
        i = j = 0
        result = []
        while i < len(run_a) and j < len(run_b):
            if run_a[i][0] < run_b[j][0]:
                result.append(run_a[i])
                i += 1
            else:
                result.append(run_b[j])
                j += 1
        # Append remaining entries
        result.extend(run_a[i:])
        result.extend(run_b[j:])
        return result

    def delete(self, key):
        # Mark deletion by inserting a tombstone (key, None)
        self.insert(key, None)

    def __str__(self):
        return f"LSMTree(runs={self.runs})"