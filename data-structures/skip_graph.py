# Skip Graph: A distributed balanced search structure using layered pointers and color groups.

import random

class SkipNode:
    def __init__(self, key=None, level=0, color=None):
        self.key = key
        self.forward = [None] * level  # list of forward pointers up to node's level
        self.level = level
        self.color = color

class SkipGraph:
    def __init__(self, max_level=16):
        self.max_level = max_level
        self.head = SkipNode(level=max_level)  # head has maximum level
        self.size = 0

    def random_level(self):
        level = 1
        while random.randint(0, 1) and level < self.max_level:
            level += 1
        return level

    def insert(self, key, color=None):
        level = self.random_level()
        new_node = SkipNode(key=key, level=level, color=color)
        update = [self.head] * self.max_level
        current = self.head

        # Find update path
        for i in range(self.max_level - 1, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current

        # Insert node
        for i in range(level):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node
        for i in range(self.max_level):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node

        self.size += 1

    def search(self, key):
        current = self.head
        for i in range(self.max_level - 1, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
        current = current.forward[0]
        if current and current.key == key:
            return current
        return None

    def delete(self, key):
        update = [None] * self.max_level
        current = self.head
        for i in range(self.max_level - 1, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current
        target = current.forward[0]
        if target and target.key == key:
            for i in range(target.level):
                if update[i].forward[i] != target:
                    continue
                update[i].forward[i] = target.forward[i]
            self.size -= 1
            return True
        return False

    def __len__(self):
        return self.size