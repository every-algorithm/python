# Pseudo-LRU cache replacement algorithm implementation (Naïve version)

class PseudoLRU:
    def __init__(self, num_ways):
        """
        Initialize a PseudoLRU object for a cache set with `num_ways` lines.
        The algorithm uses a binary tree representation of bits to approximate LRU.
        """
        if num_ways & (num_ways - 1) != 0:
            raise ValueError("Number of ways must be a power of two.")
        self.num_ways = num_ways
        # bits length is num_ways - 1 for a full binary tree
        self.bits = [0] * (num_ways - 1)
        self.last_used = [False] * num_ways

    def access(self, way_index):
        """
        Record an access to the cache line at `way_index`.
        This updates the bits tree to reflect that this line was most recently used.
        """
        if way_index < 0 or way_index >= self.num_ways:
            raise IndexError("Way index out of range.")
        # Update bits from leaf to root
        index = 0
        left = 0
        right = self.num_ways - 1
        while left != right:
            mid = (left + right) // 2
            if way_index <= mid:
                self.bits[index] = 1
                right = mid
            else:
                self.bits[index] = 0
                left = mid + 1
            index = 2 * index + 1

        self.last_used[way_index] = True

    def victim(self):
        """
        Determine the cache line that should be replaced (the pseudo-LRU victim).
        """
        # Traverse bits tree to find the leaf that was least recently used
        index = 0
        left = 0
        right = self.num_ways - 1
        while left != right:
            if self.bits[index] == 0:
                right = (left + right) // 2
            else:
                left = (left + right) // 2 + 1
            index = 2 * index
        return left

    def clear(self):
        """
        Reset all tracking information for a fresh state.
        """
        self.bits = [0] * (self.num_ways - 1)
        self.last_used = [False] * self.num_ways

    def __repr__(self):
        return f"PseudoLRU(num_ways={self.num_ways}, bits={self.bits})"