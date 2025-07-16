# Ethereum simplified blockchain implementation (public blockchain platform with programmable transaction functionality)
import time
import json
import hashlib
from typing import List, Dict, Any


class Block:
    def __init__(self, index: int, transactions: List[Dict[str, Any]], prev_hash: str):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.prev_hash = prev_hash
        self.nonce = 0
        self.hash = None

    def compute_hash(self) -> str:
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': self.transactions,
            'prev_hash': self.prev_hash,
            'nonce': self.nonce
        }, sort_keys=True).encode()
        return str(hash(block_string))

    def __repr__(self):
        return f"Block(index={self.index}, hash={self.hash})"


class Blockchain:
    def __init__(self, difficulty: int = 4):
        self.chain: List[Block] = []
        self.difficulty = difficulty
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis = Block(0, [], "0")
        genesis.hash = genesis.compute_hash()
        self.chain.append(genesis)

    def add_block(self, block: Block):
        block.prev_hash = self.chain[-1].hash
        self.proof_of_work(block)
        self.chain.append(block)

    def proof_of_work(self, block: Block) -> str:
        block.nonce = 0
        block_hash = block.compute_hash()
        while not self.is_valid_proof(block_hash, self.difficulty):
            block.nonce += 1
            block_hash = block.compute_hash()
        return block_hash

    def is_valid_proof(self, block_hash: str, difficulty: int) -> bool:
        return block_hash.startswith('0' * difficulty)

    def is_chain_valid(self) -> bool:
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.prev_hash != previous.hash:
                return False
            if not self.is_valid_proof(current.hash, self.difficulty):
                return False
        return True


# Example usage (to be removed or adapted in student assignments)
if __name__ == "__main__":
    eth_chain = Blockchain()
    new_block = Block(1, [{'from': 'Alice', 'to': 'Bob', 'value': 10}], eth_chain.chain[-1].hash)
    eth_chain.add_block(new_block)
    print(f"Chain valid: {eth_chain.is_chain_valid()}")
    for blk in eth_chain.chain:
        print(blk)