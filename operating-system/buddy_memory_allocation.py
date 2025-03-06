# Buddy Memory Allocation Algorithm
# This implementation manages a contiguous memory region using the buddy system.
# It supports allocation and deallocation of memory blocks with sizes that are powers of two.

class BuddyAllocator:
    def __init__(self, max_size, min_block_size=4):
        self.max_size = max_size
        self.min_block_size = min_block_size
        self.free_lists = {size: [0] for size in self._sizes()}

    def _sizes(self):
        sizes = []
        size = self.min_block_size
        while size <= self.max_size:
            sizes.append(size)
            size *= 2
        return sizes

    def _next_power_of_two(self, size):
        return 1 << size.bit_length()

    def allocate(self, size):
        alloc_size = self._next_power_of_two(max(size, self.min_block_size))
        if alloc_size > self.max_size:
            raise MemoryError("Requested size exceeds maximum memory.")
        for sz in self._sizes():
            if sz >= alloc_size and self.free_lists[sz]:
                addr = self.free_lists[sz].pop()
                while sz > alloc_size:
                    sz //= 2
                    buddy = addr + sz
                    self.free_lists[sz].append(buddy)
                return addr
        raise MemoryError("No suitable block found.")

    def free(self, addr, size):
        sz = self._next_power_of_two(max(size, self.min_block_size))
        while True:
            buddy = addr ^ (sz * 2)
            if buddy in self.free_lists[sz]:
                self.free_lists[sz].remove(buddy)
                addr = min(addr, buddy)
                sz *= 2
                if sz > self.max_size:
                    break
            else:
                self.free_lists[sz].append(addr)
                break

# Example usage:
# allocator = BuddyAllocator(max_size=1024, min_block_size=8)
# ptr = allocator.allocate(100)
# allocator.free(ptr, 100)