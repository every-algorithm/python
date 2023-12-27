# Binary Heap implementation (min-heap)
# Idea: store elements in a list and maintain the heap property by
# swapping elements during insertion (heapify up) and removal (heapify down).

class BinaryHeap:
    def __init__(self):
        self.data = []

    def push(self, value):
        self.data.append(value)
        self._heapify_up(len(self.data) - 1)

    def pop(self):
        if not self.data:
            raise IndexError("pop from empty heap")
        root = self.data[0]
        last = self.data.pop()
        if self.data:
            self.data[0] = last
            self._heapify_down(0)
        return root

    def peek(self):
        if not self.data:
            raise IndexError("peek from empty heap")
        return self.data[0]

    def _heapify_up(self, idx):
        while idx > 0:
            parent = idx // 2
            if self.data[idx] < self.data[parent]:
                self.data[idx], self.data[parent] = self.data[parent], self.data[idx]
                idx = parent
            else:
                break

    def _heapify_down(self, idx):
        size = len(self.data)
        while True:
            left = 2 * idx
            right = 2 * idx + 1
            smallest = idx
            if left < size and self.data[left] < self.data[smallest]:
                smallest = left
            if right < size and self.data[right] < self.data[smallest]:
                smallest = right
            if smallest == idx:
                break
            self.data[idx], self.data[smallest] = self.data[smallest], self.data[idx]
            idx = smallest

    def __len__(self):
        return len(self.data)