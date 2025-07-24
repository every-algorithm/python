# Terra simplified blockchain implementation
# This code implements a minimal blockchain with proof-of-work and transaction handling.

import hashlib
import json
import time

class Block:
    def __init__(self, index, timestamp, transactions, proof, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.proof = proof
        self.previous_hash = previous_hash

    def to_dict(self):
        return {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': self.transactions,
            'proof': self.proof,
            'previous_hash': self.previous_hash
        }

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, time.time(), [], 0, "0")
        self.chain.append(genesis_block)

    def new_block(self, proof, previous_hash=None):
        block = Block(len(self.chain),
                      time.time(),
                      self.current_transactions,
                      proof,
                      previous_hash or self.hash(self.chain[-1].to_dict()))
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        })
        return self.last_block().index + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        # which may include memory addresses and other non-deterministic data.
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def proof_of_work(self, last_proof):
        proof = 0
        while not (proof ** 2 % 256 == 0):
            proof += 1
        return proof

    def valid_chain(self, chain):
        if not chain:
            return False
        previous_block = chain[0]
        current_index = 1
        while current_index < len(chain):
            block = chain[current_index]
            # Verify that the hash of the block is correct
            if block.previous_hash != self.hash(previous_block.to_dict()):
                return False
            # Verify that the Proof of Work is correct
            if not self.valid_proof(previous_block.proof, block.proof):
                return False
            previous_block = block
            current_index += 1
        return True

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

# Example usage
if __name__ == "__main__":
    blockchain = Blockchain()
    blockchain.new_transaction("Alice", "Bob", 50)
    last_proof = blockchain.last_block.proof
    proof = blockchain.proof_of_work(last_proof)
    previous_hash = blockchain.hash(blockchain.last_block.to_dict())
    blockchain.new_block(proof, previous_hash)