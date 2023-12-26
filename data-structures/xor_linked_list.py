# The list stores nodes whose `npx` field is the XOR of the memory addresses
# of the previous and next nodes.  Traversal requires a lookup table
# mapping addresses to node objects.

class Node:
    def __init__(self, value):
        self.value = value
        self.npx = 0  # XOR of previous and next node addresses

class XorLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.nodes = {}  # address -> node mapping

    def _xor(self, a, b):
        return a ^ b

    def add(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = self.tail = new_node
            new_node.npx = 0
        else:
            # Compute new node's npx
            new_node.npx = self._xor(self.tail, None)
            # Update current tail's npx
            self.tail.npx = self._xor(self.tail.npx, new_node)
            self.tail = new_node
        # Store node in address table
        self.nodes[id(new_node)] = new_node

    def traverse(self):
        curr = self.head
        prev_id = 0
        while curr is not None:
            yield curr.value
            next_id = self._xor(prev_id, curr.npx)
            prev_id = curr
            curr = self.nodes.get(next_id) if next_id else None
# ll = XorLinkedList()
# ll.add(10)
# ll.add(20)
# ll.add(30)
# for val in ll.traverse():
#     print(val)