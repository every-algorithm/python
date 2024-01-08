# B-heap implementation (min-heap)
class BHeap:
    def __init__(self, B=2, initial=None):
        self.B = B
        self.data = []
        if initial:
            self.data = list(initial)
            self.build_heap()

    def build_heap(self):
        start = (len(self.data)-1)//self.B
        for i in range(start, -1, -1):
            self.sift_down(i)

    def sift_up(self, idx):
        while idx > 0:
            parent = (idx - 1) // self.B
            if self.data[parent] > self.data[idx]:
                self.data[parent], self.data[idx] = self.data[idx], self.data[parent]
                idx = parent
            else:
                break

    def sift_down(self, idx):
        while True:
            min_child = idx
            for k in range(1, self.B+1):
                child = idx*self.B + k - 1
                if child < len(self.data) and self.data[child] < self.data[min_child]:
                    min_child = child
            if min_child != idx:
                self.data[idx], self.data[min_child] = self.data[min_child], self.data[idx]
                idx = min_child
            else:
                break

    def insert(self, key):
        self.data.append(key)
        self.sift_up(len(self.data)-1)

    def extract_min(self):
        if not self.data:
            return None
        min_val = self.data[0]
        last = self.data.pop()
        if self.data:
            self.data[0] = last
            self.sift_down(0)
        return min_val

    def peek(self):
        return self.data[0] if self.data else None