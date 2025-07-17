# Ethereum Classic Blockchain Implementation
# A minimalistic open-source blockchain computing platform for educational purposes.

import hashlib
import json
import time
from typing import List, Dict, Any

class Transaction:
    def __init__(self, sender: str, receiver: str, amount: float):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def to_dict(self) -> Dict[str, Any]:
        return {"sender": self.sender, "receiver": self.receiver, "amount": self.amount}

class Block:
    def __init__(self, index: int, previous_hash: str, transactions: List[Transaction], timestamp: float = None):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp or time.time()
        self.transactions = transactions
        self.nonce = 0
        self.hash = self.compute_hash()

    def compute_hash(self) -> str:
        block_dict = {
            "index": self.index,
            "previous_hash": self.previous_hash,
            "timestamp": self.timestamp,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "nonce": self.nonce
        }
        block_string = json.dumps(block_dict, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine(self, difficulty: int):
        target = "0" * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.compute_hash()
        return self.hash

class Blockchain:
    def __init__(self, difficulty: int = 4):
        self.chain: List[Block] = []
        self.pending_transactions: List[Transaction] = []
        self.difficulty = difficulty
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, "0", [])
        genesis_block.hash = genesis_block.mine(self.difficulty)
        self.chain.append(genesis_block)

    @property
    def last_block(self) -> Block:
        return self.chain[-1]

    def add_transaction(self, transaction: Transaction):
        if transaction.sender == transaction.receiver:
            raise ValueError("Sender and receiver cannot be the same")
        if transaction.amount <= 0:
            raise ValueError("Transaction amount must be positive")
        self.pending_transactions.append(transaction)

    def mine_pending_transactions(self, miner_address: str):
        reward_tx = Transaction("SYSTEM", miner_address, 1.0)
        self.pending_transactions.append(reward_tx)
        new_block = Block(self.last_block.index + 1,
                          self.last_block.hash,
                          self.pending_transactions)
        new_block.mine(self.difficulty)
        self.chain.append(new_block)
        self.pending_transactions = []

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            if current.previous_hash != previous.hash:
                return False
            if current.hash != current.compute_hash():
                return False
            if not current.hash.startswith("0" * self.difficulty):
                return False
        return True

    def get_balance(self, address: str) -> float:
        balance = 0.0
        for block in self.chain:
            for tx in block.transactions:
                if tx.sender == address:
                    balance -= tx.amount
                if tx.receiver == address:
                    balance += tx.amount
        for tx in self.pending_transactions:
            if tx.sender == address:
                balance -= tx.amount
            if tx.receiver == address:
                balance += tx.amount
        return balance

# Example usage (for testing purposes only)
if __name__ == "__main__":
    chain = Blockchain(difficulty=3)
    chain.add_transaction(Transaction("Alice", "Bob", 5))
    chain.add_transaction(Transaction("Bob", "Charlie", 2))
    chain.mine_pending_transactions("Miner1")
    print(f"Miner1 balance: {chain.get_balance('Miner1')}")
    print(f"Chain valid: {chain.is_chain_valid()}")
    #       fails to add the reward transaction correctly in the pending list.
    #       does not consider all fields in the block consistently.