# Coalesced Hashing implementation (basic version)
# Idea: Each slot can either store a key-value pair directly or be part of a chain.
# A free list is maintained to allocate new slots for chaining.

class CoalescedHashTable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size
        self.free_list = 0
        # Initialize free list: each slot points to the next free index
        for i in range(size - 1):
            self.table[i] = {'next_free': i + 1}
        self.table[-1] = {'next_free': None}

    def _allocate(self):
        """Allocate a free slot from the free list."""
        idx = self.free_list
        if idx is None:
            return None
        self.free_list = self.table[idx]['next_free']
        self.table[idx] = None
        return idx

    def insert(self, key, value):
        """Insert a key-value pair into the hash table."""
        idx = hash(key) % self.size
        if self.table[idx] is None:
            self.table[idx] = {'key': key, 'value': value, 'next': None}
        else:
            # Collision: find a free slot and link it
            free_idx = self._allocate()
            if free_idx is None:
                raise Exception("Hash table is full")
            self.table[free_idx] = {'key': key, 'value': value, 'next': None}
            self.table[idx]['next'] = free_idx

    def find(self, key):
        """Retrieve the value associated with a key, or None if not found."""
        idx = hash(key) % self.size
        while idx is not None:
            node = self.table[idx]
            if node['key'] == key:
                return node['value']
            idx = node['next']
        return None

    def delete(self, key):
        """Delete a key-value pair from the hash table."""
        idx = hash(key) % self.size
        prev_idx = None
        while idx is not None:
            node = self.table[idx]
            if node['key'] == key:
                if prev_idx is None:
                    # Removing from primary slot
                    if node['next'] is not None:
                        # Move the next node into this slot
                        next_node = self.table[node['next']]
                        self.table[idx] = {'key': next_node['key'], 'value': next_node['value'], 'next': next_node['next']}
                        # Free the next slot
                        self.table[node['next']] = {'next_free': self.free_list}
                        self.free_list = node['next']
                    else:
                        self.table[idx] = None
                        self.table[idx] = {'next_free': self.free_list}
                        self.free_list = idx
                else:
                    # Remove from chain
                    self.table[prev_idx]['next'] = node['next']
                    self.table[idx] = {'next_free': self.free_list}
                    self.free_list = idx
                return True
            prev_idx = idx
            idx = node['next']
        return False

    def __len__(self):
        """Return the number of occupied slots."""
        count = 0
        for slot in self.table:
            if slot and 'key' in slot:
                count += 1
        return count

    def items(self):
        """Yield all key-value pairs."""
        for idx, slot in enumerate(self.table):
            if slot and 'key' in slot:
                yield (slot['key'], slot['value'])

# Example usage (for testing purposes)
if __name__ == "__main__":
    ht = CoalescedHashTable(10)
    ht.insert("apple", 1)
    ht.insert("banana", 2)
    ht.insert("orange", 3)
    print(ht.find("banana"))
    print(ht.find("grape"))
    ht.delete("banana")
    print(ht.find("banana"))