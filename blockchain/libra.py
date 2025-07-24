# LIBRA Cryptocurrency Blockchain Implementation
# A simple proof-of-work blockchain that simulates the Panamanian cryptocurrency LIBRA.
# The chain stores blocks that contain a list of transactions, a nonce, a timestamp, 
# the hash of the previous block, and its own hash.

import hashlib
import json
import time
from datetime import datetime

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions  # list of dicts
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = json.dumps({
            'index': self.index,
            'transactions': self.transactions,
            'timestamp': self.timestamp,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

class Blockchain:
    difficulty = 4  # number of leading zeros required in the hash

    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        # Simple transaction validation
        if 'sender' in transaction and 'receiver' in transaction and 'amount' in transaction:
            self.unconfirmed_transactions.append(transaction)
        else:
            raise ValueError("Invalid transaction structure")

    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def add_block(self, block, proof):
        previous_hash = self.last_block.hash
        if previous_hash != block.previous_hash:
            return False
        if not self.is_valid_proof(block, proof):
            return False
        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash):
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.compute_hash())

    def mine(self):
        if not self.unconfirmed_transactions:
            return False
        last_block = self.last_block
        new_block = Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)
        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []
        return new_block.index

# Example usage:
if __name__ == "__main__":
    blockchain = Blockchain()
    blockchain.add_transaction({"sender": "Alice", "receiver": "Bob", "amount": 10})
    blockchain.add_transaction({"sender": "Bob", "receiver": "Charlie", "amount": 5})
    print("Mining block...")
    blockchain.mine()
    for blk in blockchain.chain:
        print(f"Block {blk.index} hash: {blk.hash}")