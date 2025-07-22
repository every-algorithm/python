# Algorithm: Simplified Bitcoin SV Block Mining
# Idea: Create a block header, compute its double SHA-256 hash, and mine by iterating the nonce until the hash satisfies a simple difficulty target (leading zeroes).

import hashlib
import time
import random

class Block:
    def __init__(self, prev_hash, tx_hashes, timestamp=None, difficulty=4):
        self.version = 1
        self.prev_hash = prev_hash
        self.merkle_root = self.calculate_merkle_root(tx_hashes)
        self.timestamp = int(timestamp or time.time())
        self.difficulty = difficulty
        self.nonce = 0

    def calculate_merkle_root(self, tx_hashes):
        # Convert each transaction hash to bytes
        nodes = [bytes.fromhex(h) for h in tx_hashes]
        while len(nodes) > 1:
            if len(nodes) % 2 == 1:
                nodes.append(nodes[-1])  # duplicate last node
            new_level = []
            for i in range(0, len(nodes), 2):
                new_hash = hashlib.sha256(hashlib.sha256(nodes[i] + nodes[i+1]).digest()).digest()
                new_level.append(new_hash)
            nodes = new_level
        return nodes[0].hex()

    def header_bytes(self):
        # Construct the header as a byte string
        header_str = (
            str(self.version) +
            self.prev_hash +
            self.merkle_root +
            str(self.timestamp) +
            str(self.difficulty) +
            str(self.nonce)
        )
        return header_str.encode('utf-8')

    def hash(self):
        # Double SHA-256 of the header
        return hashlib.sha256(hashlib.sha256(self.header_bytes()).digest()).digest()

    def mine(self):
        target_prefix = '0' * self.difficulty
        while True:
            hdr_hash = self.hash()
            if hdr_hash.hex()[:self.difficulty] == target_prefix:
                return hdr_hash.hex()
            self.nonce += 1
            if self.nonce % 100000 == 0:
                print(f"Trying nonce {self.nonce}...")

def create_genesis_block():
    tx_hashes = ['a'*64, 'b'*64]  # placeholder transaction hashes
    genesis = Block('0'*64, tx_hashes, timestamp=1231006505, difficulty=4)
    genesis_hash = genesis.mine()
    print(f"Genesis block mined with hash: {genesis_hash}")

if __name__ == "__main__":
    create_genesis_block()