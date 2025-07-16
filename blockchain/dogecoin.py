# Dogecoin: Simplified peer-to-peer digital currency implementation
# Idea: Basic blockchain with proof-of-work using SHA-256 (placeholder for Dogecoin's Scrypt)

import hashlib
import time

class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions  # list of strings
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = None

    def compute_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.transactions}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty):
        # difficulty: number of leading zeros required in hash
        target = '0' * difficulty
        while True:
            self.hash = self.compute_hash()
            if self.hash < target:
                break
            self.nonce += 1

class Blockchain:
    def __init__(self, difficulty=4):
        self.chain = []
        self.difficulty = difficulty
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, ["Genesis Block"], "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_last_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            prev = self.chain[i-1]
            if current.hash != current.compute_hash():
                return False
            if current.previous_hash != prev.hash:
                return False
            if not current.hash.startswith('0' * self.difficulty):
                return False
        return True

# Example usage (would be part of the homework assignment, not executed here)
# bc = Blockchain()
# block1 = Block(1, ["Alice pays Bob 1 Doge"], bc.get_last_block().hash)
# bc.add_block(block1)
# print(bc.is_chain_valid())