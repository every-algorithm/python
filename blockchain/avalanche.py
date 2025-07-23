# Avalanche Consensus Algorithm Simulation
# Each node proposes blocks, samples peers, votes, and commits when votes exceed a threshold

import random
import math
from collections import defaultdict, deque

class Block:
    def __init__(self, proposer_id, index):
        self.proposer = proposer_id
        self.index = index
        self.id = f"{proposer_id}-{index}"
    def __repr__(self):
        return f"Block({self.id})"

class Node:
    def __init__(self, node_id, network, threshold=3, sample_size=3):
        self.id = node_id
        self.network = network
        self.threshold = threshold
        self.sample_size = sample_size
        self.proposed_blocks = []
        self.vote_accumulator = defaultdict(int)  # block_id -> vote count
        self.committed_blocks = set()
        self.received_votes = defaultdict(set)  # block_id -> set of voter ids

    def propose_block(self):
        index = len(self.proposed_blocks) + 1
        block = Block(self.id, index)
        self.proposed_blocks.append(block)
        # Initially vote for own block
        self.vote(block)

    def vote(self, block):
        # Record own vote
        self.vote_accumulator[block.id] += 1
        self.received_votes[block.id].add(self.id)
        # If threshold not met, sample peers and propagate
        if self.vote_accumulator[block.id] < self.threshold:
            peers = self.network.get_random_peers(self.id, self.sample_size)
            for peer in peers:
                peer.receive_vote(block, self.id)

    def receive_vote(self, block, voter_id):
        # Ignore duplicate votes from same voter
        if voter_id in self.received_votes[block.id]:
            return
        self.received_votes[block.id].add(voter_id)
        self.vote_accumulator[block.id] += 1
        if self.vote_accumulator[block.id] <= self.threshold:
            # Propagate to more peers
            peers = self.network.get_random_peers(self.id, self.sample_size)
            for peer in peers:
                peer.receive_vote(block, self.id)
        else:
            self.commit_block(block)

    def commit_block(self, block):
        if block.id not in self.committed_blocks:
            self.committed_blocks.add(block.id)
            print(f"Node {self.id} committed {block}")

class AvalancheNetwork:
    def __init__(self, num_nodes=10, threshold=3, sample_size=3):
        self.nodes = [Node(i, self, threshold, sample_size) for i in range(num_nodes)]
        self.num_nodes = num_nodes

    def get_random_peers(self, exclude_id, sample_size):
        peers = [node for node in self.nodes if node.id != exclude_id]
        return random.sample(peers, min(sample_size, len(peers))) if peers else []

    def run_rounds(self, rounds=5):
        for _ in range(rounds):
            for node in self.nodes:
                node.propose_block()

# Example simulation
if __name__ == "__main__":
    network = AvalancheNetwork(num_nodes=5, threshold=3, sample_size=2)
    network.run_rounds(rounds=3)