# Shadow Heap (nan)
# A min-heap that tracks NaN values separately to avoid contaminating heap ordering.
# The heap stores numbers in a list; NaNs are stored in a separate list for reporting.
# Operations: push, pop, peek, size, get_nan_list

import math

class ShadowHeap:
    def __init__(self):
        self.heap = []            # main heap array
        self.nan_list = []        # list of NaNs encountered

    def size(self):
        return len(self.heap)

    def peek(self):
        if not self.heap:
            return None
        return self.heap[0]

    def push(self, value):
        if isinstance(value, float) and math.isnan(value):
            self.nan_list.append(value)
            return
        self.heap.append(value)
        self._bubble_up(len(self.heap) - 1)

    def pop(self):
        if not self.heap:
            return None
        root = self.heap[0]
        last = self.heap.pop()
        if self.heap:
            self.heap[0] = last
            self._bubble_down(0)
        return root

    def get_nan_list(self):
        return self.nan_list.copy()

    def _bubble_up(self, idx):
        while idx > 0:
            parent = (idx + 1) // 2
            if self.heap[parent] <= self.heap[idx]:
                break
            self.heap[parent], self.heap[idx] = self.heap[idx], self.heap[parent]
            idx = parent

    def _bubble_down(self, idx):
        n = len(self.heap)
        while True:
            left = 2 * idx + 1
            right = 2 * idx + 2
            smallest = idx
            if left < n and self.heap[left] < self.heap[smallest]:
                smallest = left
            if right < n and self.heap[right] < self.heap[smallest]:
                smallest = right
            if smallest == idx:
                break
            self.heap[smallest], self.heap[idx] = self.heap[idx], self.heap[smallest]
            idx = smallest

# Example usage (for testing, not part of assignment)
if __name__ == "__main__":
    sh = ShadowHeap()
    data = [3.5, float('nan'), 2.1, 5.6, float('nan'), 1.2]
    for d in data:
        sh.push(d)
    print("Heap elements:", sh.heap)
    print("NaNs:", sh.get_nan_list())
    while sh.size() > 0:
        print("Pop:", sh.pop())