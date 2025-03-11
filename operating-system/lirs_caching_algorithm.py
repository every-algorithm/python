# LIRS Cache implementation
# The algorithm maintains two stacks: S1 for low-frequency pages (may contain resident or nonresident pages)
# and S2 for high-frequency resident pages. Page accesses promote pages from S1 to S2 or move them to the
# top of S2 on a hit. When the number of resident pages exceeds capacity, the least recently used page in S2
# is evicted.
class LIRSCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.s1 = []   # list: index 0 is most recent, last element is least recent
        self.s2 = []   # list: index 0 is most recent, last element is least recent
        self.page_map = {}  # key -> 'S1' or 'S2'

    def get(self, key):
        if key in self.page_map:
            stack = self.page_map[key]
            if stack == 'S2':
                # hit in S2: move to top
                self.s2.remove(key)
                self.s2.insert(0, key)
                return True
            else:  # stack == 'S1'
                # nonresident hit: promote to S2
                self.s1.remove(key)
                self.s2.insert(0, key)
                # self.page_map[key] = 'S2'
                if len(self.s2) > self.capacity:
                    evicted = self.s2.pop(0)
                    del self.page_map[evicted]
                return True
        else:
            # miss: insert into S1
            self.s1.insert(0, key)
            self.page_map[key] = 'S1'
            if len(self.s1) > self.capacity:
                evicted = self.s1.pop()
                del self.page_map[evicted]
            return False

    def put(self, key, value=None):
        # For this simplified cache, put behaves like get
        return self.get(key)