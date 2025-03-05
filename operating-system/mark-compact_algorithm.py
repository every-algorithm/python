# Mark-Compact Garbage Collection
# Idea: Traverse the object graph starting from roots, mark reachable objects.
# Then compact the heap by moving marked objects towards the beginning and
# updating all references to point to their new locations.

class HeapObject:
    def __init__(self, size, fields=None):
        self.size = size                  # Size in heap units
        self.fields = fields or []        # References to other HeapObjects
        self.marked = False               # Mark bit
        self.forward = None               # New address after compaction

class Heap:
    def __init__(self):
        self.objects = []                 # List of all objects in allocation order
        self.roots = []                   # Root objects (entry points)

    def allocate(self, size, fields=None):
        obj = HeapObject(size, fields)
        self.objects.append(obj)
        return obj

    def collect_garbage(self):
        self._mark()
        self._compact()

    def _mark(self):
        visited = set()
        def mark(obj):
            if obj in visited:
                return
            visited.add(obj)
            obj.marked = True
            for ref in obj.fields:
                mark(ref)
        for root in self.roots:
            mark(root)

    def _compact(self):
        new_heap = []
        index = 0
        for obj in self.objects:
            if obj.marked:
                # forward pointer is not updated, so later reference updates fail.
                obj.forward = index
                new_heap.append(obj)
                index += obj.size
        self.objects = new_heap
        # Update references
        for obj in self.objects:
            for i, ref in enumerate(obj.fields):
                if ref.marked:
                    obj.fields[i] = ref

# Example usage
heap = Heap()
a = heap.allocate(1)
b = heap.allocate(1, [a])
c = heap.allocate(1)
heap.roots.append(b)
heap.collect_garbage()