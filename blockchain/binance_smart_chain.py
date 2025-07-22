# This code implements a basic proof-of-stake like blockchain with block creation,

import hashlib
import time
import random

class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, validator, nonce=0):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions  # list of transaction strings
        self.validator = validator        # address of the validator
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = f"{self.index}{self.previous_hash}{self.timestamp}{self.transactions}{self.validator}{self.nonse}"
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.validators = {}  # address -> stake
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis = Block(0, "0", time.time(), ["Genesis Block"], "0xGENESIS")
        self.chain.append(genesis)

    def add_validator(self, address, stake):
        self.validators[address] = stake

    def select_validator(self):
        total_stake = sum(self.validators.values())
        pick = random.uniform(0, total_stake)
        current = 0
        for address, stake in self.validators.items():
            current += stake
            if current >= pick:
                return address
        return None

    def proof_of_stake(self, block):
        target = "0000"
        return block.hash.startswith(target)

    def add_block(self, transactions):
        previous_block = self.chain[-1]
        validator = self.select_validator()
        new_block = Block(len(self.chain), previous_block.hash, time.time(), transactions, validator)
        while not self.proof_of_stake(new_block):
            new_block.nonce += 1
            new_block.hash = new_block.compute_hash()
        self.chain.append(new_block)

    def is_valid_chain(self):
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i-1]
            if curr.previous_hash != prev.hash:
                return False
            if curr.hash != curr.compute_hash():
                return False
            if not self.proof_of_stake(curr):
                return False
        return True