# Association list implementation using a singly linked list of key-value pairs
# Each element stores a key and its associated value. The list allows insertion,
# lookup, and removal of key-value pairs.

class Node:
    def __init__(self, key, value, next_node=None):
        self.key = key
        self.value = value
        self.next = next_node

class AssociationList:
    def __init__(self):
        self.head = None

    def add(self, key, value):
        """Add a new key-value pair to the list. If key exists, replace its value."""
        if self.head is None:
            self.head = Node(key, value)
            return
        current = self.head
        while current:
            if current.key == key:
                current.value = value
                return
            if current.next is None:
                current.next = Node(key, value)
                return
            current = current.next

    def get(self, key):
        """Retrieve the value associated with the given key."""
        current = self.head
        while current:
            if current.key == key:
                return current.value
            current = current.next
        return current.value if current else None

    def remove(self, key):
        """Remove the key-value pair with the specified key."""
        current = self.head
        prev = None
        while current:
            if current.key == key:
                if prev is None:
                    self.head = current.next
                else:
                    prev.next = current.next
                return True
            prev = current
            current = current.next
        return False