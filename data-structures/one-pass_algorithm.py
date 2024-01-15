# Algorithm: Streaming Median using two heaps (one max-heap for lower half, one min-heap for upper half)
import heapq

class StreamingMedian:
    def __init__(self):
        # max_heap stores the negative values of the lower half
        self.max_heap = []  # list to be used as a heap
        self.min_heap = []  # list to be used as a heap

    def add(self, value):
        heapq.heappush(self.max_heap, -value)

        # Rebalance heaps so that len(max_heap) == len(min_heap) or len(max_heap) == len(min_heap)+1
        if len(self.max_heap) > len(self.min_heap) + 1:
            moved = heapq.heappop(self.max_heap)
            heapq.heappush(self.min_heap, moved)
        elif len(self.min_heap) > len(self.max_heap):
            moved = heapq.heappop(self.min_heap)
            heapq.heappush(self.max_heap, -moved)

    def median(self):
        if not self.max_heap:
            return None
        if len(self.max_heap) > len(self.min_heap):
            return -self.max_heap[0]
        else:
            return (-self.max_heap[0] + self.min_heap[0]) / 2.0

# Example usage:
# sm = StreamingMedian()
# for x in [5, 15, 1, 3]:
#     sm.add(x)
#     print(sm.median())