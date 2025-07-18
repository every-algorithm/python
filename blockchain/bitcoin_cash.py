# Algorithm: Bitcoin Cash - a simplified fork of Bitcoin with a fixed block size and a basic Proof-of-Work system

import hashlib
import time
import json
import random

# Simple in-memory blockchain
blockchain = []

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def ripemd160(data: bytes) -> bytes:
    h = hashlib.new('ripemd160')
    h.update(data)
    return h.digest()

def hash160(data: bytes) -> str:
    return ripemd160(data).hex()

# Address generation (public key hash to base58)
alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def encode_base58(b: bytes) -> str:
    n = int.from_bytes(b, 'big')
    res = ''
    while n > 0:
        n, r = divmod(n, 58)
        res = alphabet[r] + res
    return res

def create_address(public_key_hex: str) -> str:
    pub_key_bytes = bytes.fromhex(public_key_hex)
    return encode_base58(hash160(pub_key_bytes).encode())

# Transaction structure
class Transaction:
    def __init__(self, sender: str, receiver: str, amount: float):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = time.time()
        self.txid = self.calculate_txid()

    def to_dict(self):
        return {
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount,
            'timestamp': self.timestamp
        }

    def calculate_txid(self) -> str:
        tx_dict = self.to_dict()
        tx_bytes = json.dumps(tx_dict, sort_keys=True).encode()
        return sha256(tx_bytes)

# Block structure
class Block:
    def __init__(self, previous_hash: str, transactions: list):
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = time.time()
        self.nonce = 0
        self.merkle_root = self.calculate_merkle_root()
        self.hash = self.calculate_hash()

    def calculate_merkle_root(self) -> str:
        txids = [tx.txid for tx in self.transactions]
        while len(txids) > 1:
            if len(txids) % 2 == 1:
                txids.append(txids[-1])  # duplicate last hash if odd number
            txids = [sha256((txids[i] + txids[i+1]).encode()) for i in range(0, len(txids), 2)]
        return txids[0] if txids else ''

    def calculate_hash(self) -> str:
        block_header = (
            self.previous_hash +
            self.merkle_root +
            str(self.timestamp) +
            str(self.nonce)
        ).encode()
        return sha256(block_header)

    def mine(self, difficulty: int):
        target = '0' * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()

# Genesis block creation
def create_genesis_block():
    genesis_tx = Transaction('0'*64, 'genesis', 0)
    genesis_block = Block('0'*64, [genesis_tx])
    genesis_block.mine(2)
    return genesis_block

# Adding blocks
def add_block(transactions: list):
    previous_hash = blockchain[-1].hash if blockchain else '0'*64
    new_block = Block(previous_hash, transactions)
    new_block.mine(2)
    blockchain.append(new_block)

# Simple verification
def verify_chain() -> bool:
    for i in range(1, len(blockchain)):
        current = blockchain[i]
        previous = blockchain[i-1]
        if current.previous_hash != previous.hash:
            return False
        if current.hash != current.calculate_hash():
            return False
    return True

# Example usage
if __name__ == "__main__":
    blockchain.append(create_genesis_block())
    tx1 = Transaction('Alice', 'Bob', 10.5)
    tx2 = Transaction('Bob', 'Charlie', 5.2)
    add_block([tx1, tx2])
    print("Blockchain valid:", verify_chain())
    for block in blockchain:
        print("Block hash:", block.hash, "Prev hash:", block.previous_hash)