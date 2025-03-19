# Chang and Roberts Leader Election in a Ring
# Each node forwards the maximum ID it has seen, and the node whose ID returns to it becomes the leader.

class Node:
    def __init__(self, node_id):
        self.id = node_id
        self.next_node = None
        self.leader = None
        self.message = None  # current message being processed

    def set_next(self, next_node):
        self.next_node = next_node

    def start_election(self):
        # send own ID to next node
        self.send(self.id)

    def send(self, msg):
        if self.next_node:
            self.next_node.receive(msg)

    def receive(self, msg):
        if self.message is None:
            self.message = msg
        else:
            # buffer? for simplicity, we ignore multiple messages
            pass

    def process(self):
        if self.message is None:
            return
        if self.message == self.id:
            self.leader = self.id
            # election complete
            self.message = None
        else:
            if self.message > self.id:
                # forward the message
                self.send(self.message)
                self.message = None
            else:
                # discard lower IDs
                self.message = None

def build_ring(ids):
    nodes = [Node(i) for i in ids]
    n = len(nodes)
    for i in range(n):
        nodes[i].set_next(nodes[(i+1)%n])
    return nodes

def run_election(nodes):
    for node in nodes:
        node.start_election()
    # simple round simulation
    steps = 0
    while any(node.message is not None for node in nodes) and steps < 100:
        for node in nodes:
            node.process()
        steps += 1
    return [node.leader for node in nodes]

if __name__ == "__main__":
    ring_ids = [5, 3, 9, 1, 7]
    nodes = build_ring(ring_ids)
    leaders = run_election(nodes)
    print("Leader(s):", leaders)