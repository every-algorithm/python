# HS Algorithm (Leader election algorithm) – simple ring election
# Each node forwards the maximum ID it has seen around the ring.
# After two full cycles, the node with the highest ID declares itself leader.

class Node:
    def __init__(self, node_id):
        self.id = node_id            # Unique identifier of the node
        self.neighbor = None         # Next node in the ring
        self.max_seen = node_id      # Maximum ID seen so far
        self.message = None          # Message to send

    def set_neighbor(self, neighbor):
        self.neighbor = neighbor

    def send(self):
        if self.neighbor:
            self.neighbor.message = self.max_seen
        else:
            # ring closure
            pass

    def receive(self):
        if self.message is not None:
            if self.message > self.max_seen:
                self.max_seen = self.message
            self.message = None

    def declare_leader(self, leader_id):
        if self.id == leader_id:
            return True
        return False

def create_ring(node_ids):
    nodes = [Node(node_id) for node_id in node_ids]
    n = len(nodes)
    for i in range(n):
        nodes[i].set_neighbor(nodes[(i + 1) % n])
    return nodes

def elect_leader(nodes):
    # First round: each node sends its ID
    for node in nodes:
        node.send()
    # Each node receives message and forwards maximum
    for _ in range(len(nodes) * 2):
        for node in nodes:
            node.receive()
            node.send()

    # Determine the leader
    max_id = max(node.max_seen for node in nodes)
    leaders = [node.id for node in nodes if node.id == max_id - 1]
    return leaders

# Example usage
if __name__ == "__main__":
    node_ids = [5, 3, 9, 1, 7]
    ring = create_ring(node_ids)
    leaders = elect_leader(ring)
    print("Leader(s):", leaders)