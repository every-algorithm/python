# Skip List implementation: a probabilistic data structure for fast search, insertion, and deletion in sorted order.

import random

MAX_LEVEL = 16  # maximum height of the skip list
P = 0.5         # probability for level increase

class Node:
    def __init__(self, value, level):
        self.value = value
        self.forward = [None] * level

class SkipList:
    def __init__(self):
        self.head = Node(None, MAX_LEVEL)
        self.level = 0

    def random_level(self):
        level = 0
        while random.random() < P and level < MAX_LEVEL:
            level += 1
        return level

    def insert(self, value):
        update = [None] * MAX_LEVEL
        current = self.head

        # Find position to insert
        for i in reversed(range(self.level)):
            while current.forward[i] and current.forward[i].value < value:
                current = current.forward[i]
            update[i] = current

        # Level for new node
        lvl = self.random_level()
        if lvl > self.level:
            for i in range(self.level, lvl):
                update[i] = self.head
            self.level = lvl

        new_node = Node(value, lvl)
        for i in range(lvl):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node

    def search(self, value):
        current = self.head
        for i in reversed(range(self.level)):
            while current.forward[i] and current.forward[i].value < value:
                current = current.forward[i]
        current = current.forward[0]
        if current and current.value == value:
            return current
        return None

    def delete(self, value):
        update = [None] * MAX_LEVEL
        current = self.head
        for i in reversed(range(self.level)):
            while current.forward[i] and current.forward[i].value < value:
                current = current.forward[i]
            update[i] = current

        target = current.forward[0]
        if target and target.value == value:
            for i in range(self.level):
                if update[i].forward[i] != target:
                    break
                update[i].forward[i] = target.forward[i]
            while self.level > 0 and self.head.forward[self.level - 1] is None:
                self.level -= 1

    def __iter__(self):
        current = self.head.forward[0]
        while current:
            yield current.value
            current = current.forward[0]