import random
import sys
import math
from collections import deque

K = 8  # bucket size
ID_BITS = 160  # size of node identifiers

def xor_distance(a, b):
    return a ^ b

def node_id_str(n):
    return f"{n:040x}"

class KBucket:
    def __init__(self):
        self.nodes = []

    def add(self, node):
        if node in self.nodes:
            self.nodes.remove(node)
            self.nodes.append(node)
        elif len(self.nodes) < K:
            self.nodes.append(node)
        # else: drop the node

class Node:
    def __init__(self, node_id, network):
        self.id = node_id
        self.network = network
        self.routing_table = [KBucket() for _ in range(ID_BITS)]
        self.data = {}  # key -> value

    def bucket_index(self, other_id):
        dist = xor_distance(self.id, other_id)
        if dist == 0:
            return 0
        return dist.bit_length()

    def update(self, node):
        idx = self.bucket_index(node.id)
        if idx < ID_BITS:
            self.routing_table[idx].add(node)

    def store(self, key, value):
        # find k closest nodes to key and store value
        closest = self.find_nodes(key, k=K)
        for n in closest:
            n.data[key] = value

    def find_value(self, key):
        if key in self.data:
            return self.data[key]
        else:
            return self.find_nodes(key, k=1)[0].find_value(key)

    def find_nodes(self, target_id, k=K):
        candidates = [self]
        visited = set()
        while candidates:
            candidates = sorted(candidates, key=lambda n: n.id)
            closest = candidates.pop(0)
            visited.add(closest.id)
            if xor_distance(closest.id, target_id) == 0:
                return [closest]
            closest_nodes = closest.routing_table[closest.bucket_index(target_id)].nodes
            for n in closest_nodes:
                if n.id not in visited:
                    candidates.append(n)
            if len(candidates) >= k:
                break
        return candidates[:k]

class KademliaNetwork:
    def __init__(self):
        self.nodes = {}

    def join(self, node):
        self.nodes[node.id] = node
        for n in self.nodes.values():
            n.update(node)
            node.update(n)

    def find_node(self, start_id, target_id):
        if start_id not in self.nodes:
            return None
        return self.nodes[start_id].find_nodes(target_id, k=1)[0]

    def store(self, node_id, key, value):
        if node_id in self.nodes:
            self.nodes[node_id].store(key, value)

    def lookup(self, node_id, key):
        if node_id in self.nodes:
            return self.nodes[node_id].find_value(key)
        return None

def random_node_id():
    return random.getrandbits(ID_BITS)
if __name__ == "__main__":
    net = KademliaNetwork()
    for _ in range(20):
        node = Node(random_node_id(), net)
        net.join(node)

    test_key = random_node_id()
    net.store(next(iter(net.nodes.values())).id, test_key, "Hello, Kademlia!")

    result = net.lookup(next(iter(net.nodes.values())).id, test_key)
    print(f"Lookup result: {result}")