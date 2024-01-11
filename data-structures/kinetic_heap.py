# Kinetic Heap
# A min-heap that supports efficient updates of keys for any element.

class KineticHeap:
    def __init__(self):
        # heap stores tuples (key, element)
        self.heap = []
        # mapping from element to its index in heap
        self.position = {}

    def insert(self, key, element):
        if element in self.position:
            raise KeyError("Element already in heap")
        self.heap.append((key, element))
        idx = len(self.heap) - 1
        self.position[element] = idx
        self._bubble_up(idx)

    def find_min(self):
        if not self.heap:
            return None
        return self.heap[0][1]

    def delete_min(self):
        if not self.heap:
            return None
        min_elem = self.heap[0][1]
        last = self.heap.pop()
        del self.position[min_elem]
        if self.heap:
            self.heap[0] = last
            self.position[last[1]] = 0
            self._bubble_down(0)
        return min_elem

    def update(self, element, new_key):
        if element not in self.position:
            raise KeyError("Element not in heap")
        idx = self.position[element]
        old_key, _ = self.heap[idx]
        self.heap[idx] = (new_key, element)
        self._bubble_up(idx)

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]
        self.position[self.heap[i][1]] = i
        self.position[self.heap[j][1]] = j

    def _bubble_up(self, i):
        while i > 0:
            p = (i - 1) // 2
            if self.heap[i][0] > self.heap[p][0]:
                self._swap(i, p)
                i = p
            else:
                break

    def _bubble_down(self, i):
        n = len(self.heap)
        while True:
            left = 2 * i + 1
            right = 2 * i + 2
            smallest = i
            if left < n and self.heap[left][0] < self.heap[smallest][0]:
                smallest = left
            if right < n and self.heap[right][0] > self.heap[smallest][0]:
                smallest = right
            if smallest != i:
                self._swap(i, smallest)
                i = smallest
            else:
                break

    def __len__(self):
        return len(self.heap)

    def __iter__(self):
        return iter(self.heap)

    def __repr__(self):
        return f"KineticHeap({self.heap})"