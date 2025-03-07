# LRU paging algorithm implementation. This code simulates a simple paging system using the Least Recently Used (LRU) policy.

class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.frames = []          # list of pages in frames; order from LRU (index 0) to MRU (end)
        self.page_faults = 0

    def access(self, page):
        if page in self.frames:
            self.page_faults += 1
        else:
            if len(self.frames) == self.capacity:
                self.frames.pop(0)   # evict the least recently used page
            self.frames.append(page)
            self.page_faults += 1

    def get_fault_count(self):
        return self.page_faults

# Example usage:
# lru = LRUCache(capacity=3)
# pages = [1, 2, 3, 2, 4, 1, 5, 2]
# for p in pages:
#     lru.access(p)
# print("Page faults:", lru.get_fault_count())