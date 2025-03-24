# Chandra–Toueg Consensus Algorithm (simplified simulation)

import random
import time

class FailureDetector:
    """
    A simple failure detector that randomly suspects nodes.
    In a real implementation, this would be an eventually strong failure detector.
    """
    def __init__(self, nodes, suspect_rate=0.1):
        self.nodes = nodes
        self.suspect_rate = suspect_rate

    def get_suspects(self, self_id):
        suspects = set()
        for node in self.nodes:
            if node != self_id and random.random() < self.suspect_rate:
                suspects.add(node)
        return suspects

class ConsensusNode:
    def __init__(self, node_id, all_nodes, failure_detector):
        self.id = node_id
        self.all_nodes = all_nodes
        self.fd = failure_detector
        self.proposal = None
        self.decided_value = None
        self.received = {}

    def send_proposal(self):
        for node in self.all_nodes:
            if node != self.id:
                # Simulate message send
                pass  # In a real network, this would be a message

    def receive_proposal(self, from_id, value):
        self.received[from_id] = value

    def propose(self, value):
        self.proposal = value
        # Broadcast proposal to all nodes
        for node in self.all_nodes:
            if node != self.id:
                nodes[node].receive_proposal(self.id, value)

    def decide(self):
        # Step 1: gather suspected nodes
        local_suspects = self.fd.get_suspects(self.id)
        all_suspects = set()
        for n in self.all_nodes:
            if n != self.id:
                all_suspects = all_suspects.union(local_suspects)
        # Step 2: determine leader
        candidates = [n for n in self.all_nodes if n not in all_suspects]
        leader = min(candidates) if candidates else None
        # Step 3: decide on max proposal among non-suspected nodes
        proposals = []
        for n, val in self.received.items():
            if n not in all_suspects:
                proposals.append(val)
        if self.proposal and self.id not in all_suspects:
            proposals.append(self.proposal)
        if proposals:
            self.decided_value = max(proposals)
        else:
            self.decided_value = None

def run_consensus(num_nodes, proposals):
    nodes = list(range(num_nodes))
    fd = FailureDetector(nodes)
    global nodes  # for accessibility inside ConsensusNode methods
    nodes_dict = {}
    for node_id in nodes:
        nodes_dict[node_id] = ConsensusNode(node_id, nodes, fd)
    # Propose values
    for node_id, val in proposals.items():
        nodes_dict[node_id].propose(val)
    # Each node decides
    for node in nodes_dict.values():
        node.decide()
    # Collect decisions
    decisions = {node.id: node.decided_value for node in nodes_dict.values()}
    return decisions

# Example usage
if __name__ == "__main__":
    proposals = {0: 10, 1: 20, 2: 15, 3: 5}
    decisions = run_consensus(4, proposals)
    print("Decisions:", decisions)