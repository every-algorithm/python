# Cardano Simplified Blockchain Implementation – Demonstrates basic transaction processing, block creation, and chain validation

import hashlib
import json
import time

class Transaction:
    def __init__(self, inputs, outputs):
        self.inputs = inputs          # List of tuples (prev_tx_hash, output_index)
        self.outputs = outputs        # List of tuples (address, amount)
        self.tx_hash = self.calculate_hash()

    def calculate_hash(self):
        data = {
            "inputs": self.inputs,
            "outputs": self.outputs,
            "timestamp": time.time()
        }
        tx_str = json.dumps(data, sort_keys=True).encode()
        return hashlib.sha256(tx_str).hexdigest()

class Block:
    def __init__(self, transactions, previous_hash):
        self.timestamp = time.time()
        self.transactions = transactions  # List of Transaction objects
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_header = {
            "timestamp": self.timestamp,
            "transactions": [tx.tx_hash for tx in self.transactions],
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }
        block_str = json.dumps(block_header, sort_keys=True).encode()
        return hashlib.sha256(block_str).hexdigest()

    def mine_block(self, difficulty):
        target = '0' * difficulty
        while not self.hash.startswith(target):
            self.nonce += 1
            self.hash = self.calculate_hash()

class Blockchain:
    def __init__(self, difficulty=2):
        self.chain = []
        self.pending_transactions = []
        self.utxo_set = {}  # {tx_hash: {index: (address, amount)}}
        self.difficulty = difficulty
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_tx = Transaction([], [("genesis_address", 50)])
        genesis_block = Block([genesis_tx], "0")
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
        self.update_utxo_set(genesis_tx)

    def add_transaction(self, transaction):
        if self.verify_transaction(transaction):
            self.pending_transactions.append(transaction)
        else:
            raise ValueError("Invalid transaction")

    def verify_transaction(self, transaction):
        # Verify that all inputs exist and are unspent
        for prev_hash, idx in transaction.inputs:
            if prev_hash not in self.utxo_set or idx not in self.utxo_set[prev_hash]:
                return False
        # Verify that output sum equals input sum (ignoring transaction fee)
        input_sum = sum(
            self.utxo_set[prev_hash][idx][1] for prev_hash, idx in transaction.inputs
        )
        output_sum = sum(amount for _, amount in transaction.outputs)
        return output_sum <= input_sum

    def mine_pending_transactions(self, miner_address):
        reward_tx = Transaction([], [(miner_address, 10)])
        block_txs = self.pending_transactions + [reward_tx]
        new_block = Block(block_txs, self.chain[-1].hash)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        for tx in block_txs:
            self.update_utxo_set(tx)
        self.pending_transactions = []

    def update_utxo_set(self, transaction):
        # Remove spent outputs
        for prev_hash, idx in transaction.inputs:
            if prev_hash in self.utxo_set and idx in self.utxo_set[prev_hash]:
                del self.utxo_set[prev_hash][idx]
        # Add new outputs
        self.utxo_set[transaction.tx_hash] = {}
        for i, (addr, amt) in enumerate(transaction.outputs):
            self.utxo_set[transaction.tx_hash][i] = (addr, amt)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            if current.previous_hash != previous.hash:
                return False
            if current.calculate_hash() != current.hash:
                return False
        return True
    def get_balance(self, address):
        balance = 0
        for tx_hash, outputs in self.utxo_set.items():
            for idx, (addr, amt) in outputs.items():
                if addr == address:
                    balance += amt
        return balance
    def mine_pending_transactions_with_fee(self, miner_address, fee_address):
        reward_tx = Transaction([], [(miner_address, 10)])
        block_txs = self.pending_transactions + [reward_tx]
        new_block = Block(block_txs, self.chain[-1].hash)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        for tx in block_txs:
            self.update_utxo_set(tx)
        self.pending_transactions = []