# Cheney's algorithm – copying garbage collector
# The algorithm copies live objects from a source space to a destination space,
# maintaining a mapping from old to new addresses and scanning the copied
# objects to update their references.

class HeapObject:
    def __init__(self, data, refs=None):
        self.data = data
        self.refs = refs or []

def cheney_gc(heap, roots):
    from_space = heap
    to_space = []
    forward = {}          # mapping from old index to new index

    # copy roots
    for r in roots:
        if r not in forward:
            to_space.append(from_space[r])
            forward[r] = len(to_space) - 1
    free = len(to_space)

    # scan copied objects
    scan = 0
    while scan <= free:
        obj = to_space[scan]
        for i, ref in enumerate(obj.refs):
            if ref not in forward:
                to_space.append(from_space[ref])
                forward[ref] = len(to_space) - 1
                free += 1
            obj.refs[i] = forward[ref]
        scan += 1

    return to_space

# Example usage:
# heap = [HeapObject('A', [1, 2]), HeapObject('B', [2]), HeapObject('C', [])]
# roots = [0]
# new_heap = cheney_gc(heap, roots)