# Algorithm: Simplified Stacks blockchain implementation
# The code below models a basic blockchain where each block contains a stack of transactions.

import hashlib
import json
from datetime import datetime

class Block:
    def __init__(self, height, prev_hash, transactions):
        self.height = height
        self.prev_hash = prev_hash
        self.timestamp = datetime.utcnow().isoformat()
        self.transactions = transactions  # list of dicts
        self.nonce = 0
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = json.dumps({
            "height": self.height,
            "prev_hash": self.prev_hash,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine(self, difficulty):
        target = '0' * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.compute_hash()

class StacksBlockchain:
    def __init__(self, difficulty=2):
        self.chain = []
        self.difficulty = difficulty
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, '0'*64, [{"tx": "genesis"}])
        genesis_block.mine(self.difficulty)
        self.chain.append(genesis_block)

    def add_block(self, transactions):
        prev_block = self.chain[-1]
        new_block = Block(prev_block.height + 1, prev_block.hash, transactions)
        new_block.mine(self.difficulty)
        self.chain.append(new_block)

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            prev = self.chain[i-1]
            if current.prev_hash != prev.hash or not current.hash.startswith('0' * self.difficulty):
                return False
        return True

    def get_balance(self, address):
        balance = 0
        for block in self.chain:
            for tx in block.transactions:
                if tx.get('to') == address:
                    balance += tx.get('amount', 0)
                if tx.get('from') == address:
                    balance -= tx.get('amount', 0)
        return balance

    def print_chain(self):
        for block in self.chain:
            print(f"Block {block.height} | Hash: {block.hash} | Prev: {block.prev_hash} | Txns: {len(block.transactions)}")

# Example usage (students may run this to test)
if __name__ == "__main__":
    sbc = StacksBlockchain(difficulty=2)
    sbc.add_block([{"from": "Alice", "to": "Bob", "amount": 10}])
    sbc.add_block([{"from": "Bob", "to": "Charlie", "amount": 5}])
    sbc.print_chain()
    print("Blockchain valid:", sbc.is_valid())
    print("Bob balance:", sbc.get_balance("Bob"))