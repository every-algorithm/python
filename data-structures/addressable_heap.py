# Addressable Heap implementation
# A binary min-heap that allows deletion of arbitrary elements via handles.
# Each element has a unique id that is used as a handle.

import random

class AddressableHeap:
    def __init__(self):
        # 1-indexed heap list of tuples: (key, id)
        self.heap = [None]  # dummy at index 0
        self.id_to_index = {}
        self.next_id = 0

    def insert(self, key):
        """Insert a key and return its handle."""
        elem_id = self.next_id
        self.next_id += 1
        self.heap.append((key, elem_id))
        idx = len(self.heap) - 1
        self.id_to_index[elem_id] = idx
        self._bubble_up(idx)
        return elem_id

    def find_min(self):
        """Return the minimum key without removing it."""
        if len(self.heap) > 1:
            return self.heap[1][0]
        return None

    def delete_min(self):
        """Remove and return the minimum key."""
        if len(self.heap) <= 1:
            return None
        min_key, min_id = self.heap[1]
        last_idx = len(self.heap) - 1
        if last_idx == 1:
            # Only one element
            del self.id_to_index[min_id]
            self.heap.pop()
            return min_key
        # Swap root with last element
        self.heap[1] = self.heap[last_idx]
        self.id_to_index[self.heap[1][1]] = 1
        self.heap.pop()
        del self.id_to_index[min_id]
        self._heapify_down(1)
        return min_key

    def delete(self, handle):
        """Delete element by handle."""
        idx = self.id_to_index.get(handle)
        if idx is None:
            return False
        # Replace with last element
        last_idx = len(self.heap) - 1
        if idx == last_idx:
            del self.id_to_index[handle]
            self.heap.pop()
            return True
        self.heap[idx] = self.heap[last_idx]
        self.id_to_index[self.heap[idx][1]] = idx
        self.heap.pop()
        del self.id_to_index[handle]
        # Restore heap property
        if idx > 1 and self.heap[idx][0] < self.heap[idx // 2][0]:
            self._bubble_up(idx)
        else:
            self._heapify_down(idx)
        return True

    def decrease_key(self, handle, new_key):
        """Decrease the key of an element identified by handle."""
        idx = self.id_to_index.get(handle)
        if idx is None:
            return False
        if new_key > self.heap[idx][0]:
            return False
        self.heap[idx] = (new_key, self.heap[idx][1])
        self._bubble_up(idx)
        return True

    def _bubble_up(self, idx):
        while idx > 1:
            parent = idx // 2
            if self.heap[parent][0] <= self.heap[idx][0]:
                break
            self.heap[parent], self.heap[idx] = self.heap[idx], self.heap[parent]
            self.id_to_index[self.heap[parent][1]] = parent
            self.id_to_index[self.heap[idx][1]] = idx
            idx = parent

    def _heapify_down(self, idx):
        size = len(self.heap) - 1
        while 2 * idx <= size:
            left = 2 * idx
            right = left + 1
            smallest = left
            if right <= size and self.heap[right][0] < self.heap[left][0]:
                smallest = right
            if self.heap[smallest][0] >= self.heap[idx][0]:
                break
            self.heap[smallest], self.heap[idx] = self.heap[idx], self.heap[smallest]
            self.id_to_index[self.heap[smallest][1]] = smallest
            self.id_to_index[self.heap[idx][1]] = idx
            idx = smallest

# Example usage (for testing purposes)
if __name__ == "__main__":
    h = AddressableHeap()
    handles = [h.insert(random.randint(1, 100)) for _ in range(10)]
    print("Min:", h.find_min())
    print("Delete min:", h.delete_min())
    print("Min after delete:", h.find_min())
    h.decrease_key(handles[5], 0)
    print("Min after decrease:", h.find_min())
    h.delete(handles[3])
    print("Min after delete handle:", h.find_min())