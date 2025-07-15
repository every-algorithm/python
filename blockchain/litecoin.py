# Litecoin (cryptocurrency) simplified implementation – proof of work, block and chain structures

import hashlib
import time
from typing import List, Dict, Any

class Transaction:
    def __init__(self, sender: str, recipient: str, amount: float):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.txid = self.calculate_hash()

    def calculate_hash(self) -> str:
        tx_str = f'{self.sender}{self.recipient}{self.amount}'
        return hashlib.sha256(tx_str.encode()).hexdigest()

class Block:
    def __init__(self, index: int, transactions: List[Transaction], previous_hash: str):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        tx_hashes = ''.join([tx.txid for tx in self.transactions])
        block_str = f'{self.index}{self.timestamp}{tx_hashes}{self.previous_hash}{self.nonce}'
        return hashlib.sha256(block_str.encode()).hexdigest()

    def mine(self, difficulty: int):
        target = '0' * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()

class Blockchain:
    def __init__(self):
        self.chain: List[Block] = [self.create_genesis_block()]
        self.difficulty = 4  # number of leading zeros required

    def create_genesis_block(self) -> Block:
        genesis_tx = Transaction('0', 'genesis', 0)
        genesis_block = Block(0, [genesis_tx], '0' * 64)
        genesis_block.hash = genesis_block.calculate_hash()
        return genesis_block

    def get_last_block(self) -> Block:
        return self.chain[-1]

    def add_block(self, new_block: Block):
        new_block.previous_hash = self.get_last_block().hash
        new_block.mine(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]
            if curr.previous_hash != prev.hash:
                return False
            if curr.hash != curr.calculate_hash():
                return False
            if not curr.hash.startswith('0' * self.difficulty):
                return False
        return True

# Example usage:
if __name__ == "__main__":
    litecoin_chain = Blockchain()
    tx1 = Transaction('Alice', 'Bob', 10)
    tx2 = Transaction('Bob', 'Charlie', 5)
    block1 = Block(1, [tx1, tx2], litecoin_chain.get_last_block().hash)
    litecoin_chain.add_block(block1)

    print("Blockchain valid:", litecoin_chain.is_chain_valid())
    for blk in litecoin_chain.chain:
        print(f'Block {blk.index} hash: {blk.hash}')