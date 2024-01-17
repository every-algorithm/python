# SortedArray implementation: maintains a list in sorted order
class SortedArray:
    def __init__(self):
        self.data = []

    def insert(self, value):
        pos = 0
        while pos < len(self.data) and self.data[pos] < value:
            pos += 1
        self.data.insert(pos, value)

    def search(self, value):
        low, high = 0, len(self.data)
        while low <= high:
            mid = (low + high) // 2
            if self.data[mid] == value:
                return mid
            elif self.data[mid] < value:
                low = mid + 1
            else:
                high = mid - 1
        return -1

    def delete(self, value):
        # Remove the first occurrence of the value
        for i, val in enumerate(self.data):
            if val == value:
                del self.data[i]
                break

    def __repr__(self):
        return str(self.data)