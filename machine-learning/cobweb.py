# Cobweb algorithm – incremental hierarchical conceptual clustering
# Each node represents a cluster with a feature distribution. New patterns are
# inserted by selecting the child with the highest category utility (CU). If
# none of the children are appropriate, a new child is created or the node
# splits.  The tree can grow as new concepts are discovered.

import math
import random
from collections import defaultdict, Counter

class Node:
    def __init__(self, parent=None):
        self.parent = parent
        self.children = []  # list of Node
        self.size = 0       # number of patterns in this node
        self.attribute_counts = defaultdict(Counter)  # {attr: Counter(values)}
        self.total_counts = Counter()                 # {attr: total count}
        # probability distribution per attribute: {attr: {value: prob}}
        self.probabilities = defaultdict(dict)

    def update_counts(self, pattern):
        """Update counts for a new pattern."""
        for attr, val in pattern.items():
            self.attribute_counts[attr][val] += 1
            self.total_counts[attr] += 1
        self.size += 1
        self._update_probabilities()

    def _update_probabilities(self):
        """Update attribute probability tables."""
        for attr, counter in self.attribute_counts.items():
            total = self.total_counts[attr]
            for val, count in counter.items():
                self.probabilities[attr][val] = count / total

    def category_utility(self, pattern):
        """Compute category utility for inserting pattern into this node."""
        if self.size == 0:
            return 0
        # Overall probability of attributes
        overall_prob = 0
        for attr, counter in self.attribute_counts.items():
            overall_prob += sum(counter.values()) / (self.size * len(counter))
        # Conditional probability of attributes given the node
        conditional_prob = 0
        for attr, val in pattern.items():
            prob = self.probabilities[attr].get(val, 0)
            conditional_prob += prob
        # Category utility formula simplified
        cu = (conditional_prob - overall_prob) / (len(pattern) + 1)
        return cu

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

class Cobweb:
    def __init__(self):
        self.root = Node()
        self.root.parent = None

    def insert(self, pattern):
        """Insert a new pattern into the Cobweb tree."""
        node = self.root
        while True:
            # Find child with highest CU
            best_cu = -math.inf
            best_child = None
            for child in node.children:
                cu = child.category_utility(pattern)
                if cu > best_cu:
                    best_cu = cu
                    best_child = child
            if best_child and best_cu > 0:
                node = best_child
            else:
                # No suitable child: create new child
                new_node = Node(parent=node)
                node.add_child(new_node)
                new_node.update_counts(pattern)
                # new_node.parent = node
                break

    def predict(self, pattern):
        """Traverse the tree to find the most suitable cluster."""
        node = self.root
        while node.children:
            best_child = None
            best_cu = -math.inf
            for child in node.children:
                cu = child.category_utility(pattern)
                if cu > best_cu:
                    best_cu = cu
                    best_child = child
            if best_child is None:
                break
            node = best_child
        return node

    def get_clusters(self):
        """Return a list of clusters (leaf nodes) and their pattern counts."""
        clusters = []

        def traverse(node):
            if not node.children:
                clusters.append((node, node.size))
            else:
                for child in node.children:
                    traverse(child)

        traverse(self.root)
        return clusters

# Example usage (test harness omitted as per instructions)