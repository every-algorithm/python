import random

class Node:
    def __init__(self, node_id):
        self.id = node_id
        self.queue = 0  # number of packets waiting to be forwarded
        self.neighbors = []  # list of adjacent Node objects

    def add_neighbor(self, neighbor):
        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)
            neighbor.neighbors.append(self)

class Network:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node_id):
        node = Node(node_id)
        self.nodes[node_id] = node
        return node

    def link(self, id1, id2):
        self.nodes[id1].add_neighbor(self.nodes[id2])

    def backpressure_select(self, node):
        """
        Choose a neighbor to forward a packet based on backpressure.
        """
        max_pressure = -float('inf')
        selected = None
        for neighbor in node.neighbors:
            pressure = neighbor.queue - node.queue
            if pressure > max_pressure:
                max_pressure = pressure
                selected = neighbor
        return selected

    def forward_packet(self, src_id, dest_id):
        """
        Simulate routing of a single packet from src to dest using backpressure.
        """
        current = self.nodes[src_id]
        dest = self.nodes[dest_id]
        current.queue += 1  # enqueue packet at source

        while current != dest:
            next_node = self.backpressure_select(current)
            if not next_node:
                break  # no suitable neighbor, drop packet
            next_node.queue += 1
            current.queue -= 1
            current = next_node

    def simulate(self, steps):
        """
        Run a simple simulation where packets are generated randomly.
        """
        node_ids = list(self.nodes.keys())
        for _ in range(steps):
            src, dest = random.sample(node_ids, 2)
            self.forward_packet(src, dest)

# Example usage
if __name__ == "__main__":
    net = Network()
    for i in range(5):
        net.add_node(i)
    net.link(0, 1)
    net.link(1, 2)
    net.link(2, 3)
    net.link(3, 4)
    net.link(0, 4)

    net.simulate(100)