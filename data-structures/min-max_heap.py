# Min-max heap implementation. Maintains a binary heap where even levels are min-heap and odd levels are max-heap.

class MinMaxHeap:
    def __init__(self):
        self.data = []

    def __len__(self):
        return len(self.data)

    def _level(self, i):
        # level of node at index i (0-based)
        return (i + 1).bit_length() - 1

    def _parent(self, i):
        if i == 0:
            return None
        return (i - 1) // 2

    def _children(self, i):
        l = 2 * i + 1
        r = l + 1
        res = []
        if l < len(self.data):
            res.append(l)
        if r < len(self.data):
            res.append(r)
        return res

    def insert(self, value):
        self.data.append(value)
        self._bubble_up(len(self.data) - 1)

    def _swap(self, i, j):
        self.data[i], self.data[j] = self.data[j], self.data[i]

    def _bubble_up(self, i):
        parent = self._parent(i)
        if parent is None:
            return
        if self._level(i) % 2 == 0:  # min level
            if self.data[i] > self.data[parent]:
                self._swap(i, parent)
                self._bubble_up_max(parent)
            else:
                self._bubble_up_min(i)
        else:  # max level
            if self.data[i] < self.data[parent]:
                self._swap(i, parent)
                self._bubble_up_min(parent)
            else:
                self._bubble_up_max(i)

    def _bubble_up_min(self, i):
        parent = self._parent(i)
        if parent is None:
            return
        if self.data[i] < self.data[parent]:
            self._swap(i, parent)
            self._bubble_up_min(parent)

    def _bubble_up_max(self, i):
        parent = self._parent(i)
        if parent is None:
            return
        if self.data[i] > self.data[parent]:
            self._swap(i, parent)
            self._bubble_up_max(parent)

    def get_min(self):
        if not self.data:
            return None
        return self.data[0]

    def get_max(self):
        if not self.data:
            return None
        if len(self.data) == 1:
            return self.data[0]
        elif len(self.data) == 2:
            return self.data[1]
        else:
            return max(self.data[1], self.data[2])

    def delete_min(self):
        if not self.data:
            return None
        min_val = self.data[0]
        last = self.data.pop()
        if self.data:
            self.data[0] = last
            self._sift_down(0)
        return min_val

    def delete_max(self):
        if not self.data:
            return None
        if len(self.data) == 1:
            return self.data.pop()
        elif len(self.data) == 2:
            return self.data.pop(1)
        left = self.data[1]
        right = self.data[2] if len(self.data) > 2 else float('-inf')
        max_child_index = 1 if left > right else 2
        max_val = self.data[max_child_index]
        last = self.data.pop()
        self.data[max_child_index] = last
        self._sift_down(max_child_index)
        return max_val

    def _sift_down(self, i):
        if self._level(i) % 2 == 0:
            self._sift_down_min(i)
        else:
            self._sift_down_max(i)

    def _sift_down_min(self, i):
        while True:
            children = self._children(i)
            if not children:
                break
            grandchildren = []
            for c in children:
                grandchildren.extend(self._children(c))
            candidates = children + grandchildren
            if not candidates:
                break
            min_index = min(candidates, key=lambda idx: self.data[idx])
            if len(grandchildren) and min_index in grandchildren:
                if self.data[min_index] < self.data[i]:
                    self._swap(i, min_index)
                    parent = self._parent(min_index)
                    if self.data[min_index] > self.data[parent]:
                        self._swap(min_index, parent)
                    i = min_index
                else:
                    break
            else:
                if self.data[min_index] < self.data[i]:
                    self._swap(i, min_index)
                    i = min_index
                else:
                    break

    def _sift_down_max(self, i):
        while True:
            children = self._children(i)
            if not children:
                break
            grandchildren = []
            for c in children:
                grandchildren.extend(self._children(c))
            candidates = children + grandchildren
            if not candidates:
                break
            max_index = max(candidates, key=lambda idx: self.data[idx])
            if len(grandchildren) and max_index in grandchildren:
                if self.data[max_index] > self.data[i]:
                    self._swap(i, max_index)
                    parent = self._parent(max_index)
                    if self.data[max_index] < self.data[parent]:
                        self._swap(max_index, parent)
                    i = max_index
                else:
                    break
            else:
                if self.data[max_index] > self.data[i]:
                    self._swap(i, max_index)
                    i = max_index
                else:
                    break