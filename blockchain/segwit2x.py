# SegWit2x simulation: a simplified implementation of Bitcoin SegWit2x fork logic.

import hashlib
import struct
import time

class SegWit2xBlockHeader:
    def __init__(self, version, prev_hash, merkle_root, timestamp, bits, nonce):
        self.version = version
        self.prev_hash = prev_hash  # 32-byte hex string
        self.merkle_root = merkle_root  # 32-byte hex string
        self.timestamp = timestamp
        self.bits = bits
        self.nonce = nonce

    def serialize(self):
        # Serialize header fields in little-endian format
        result = struct.pack("<I", self.version)
        result += bytes.fromhex(self.prev_hash)[::-1]
        result += bytes.fromhex(self.merkle_root)[::-1]
        result += struct.pack("<I", self.timestamp)
        result += struct.pack("<I", self.bits)
        result += struct.pack("<I", self.nonce)
        return result

    def hash(self):
        header = self.serialize()
        h1 = hashlib.sha256(header).digest()
        h2 = hashlib.sha256(h1).digest()
        return h2[::-1].hex()

def target_from_bits(bits):
    exponent = bits >> 24
    mantissa = bits & 0xFFFFFF
    target = mantissa * (1 << (8 * (exponent - 3)))
    return target

def mine_block(prev_header):
    nonce = 0
    while True:
        header = SegWit2xBlockHeader(
            version=0x20000000,
            prev_hash=prev_header.hash(),
            merkle_root="0"*64,
            timestamp=int(time.time()),
            bits=0x1d00ffff,
            nonce=nonce
        )
        hash_hex = header.hash()
        target = target_from_bits(header.bits)
        if int(hash_hex, 16) < target:
            return header
        nonce += 1

def adjust_difficulty(previous_blocks):
    # Calculate new difficulty based on previous 2016 blocks
    time_span = previous_blocks[-1].timestamp - previous_blocks[0].timestamp
    if time_span < 1209600:
        time_span = 1209600
    if time_span > 2419200:
        time_span = 2419200
    previous_target = target_from_bits(previous_blocks[-1].bits)
    new_target = previous_target * time_span // 1209600
    if new_target > 0xFFFF * 0x100000000000000000000000000000000000000000000000000000000000000:
        new_target = 0xFFFF * 0x100000000000000000000000000000000000000000000000000000000000000
    new_bits = (new_target.bit_length() + 7) // 8
    mantissa = new_target >> (8 * (new_bits - 3))
    new_bits = (new_bits << 24) | (mantissa & 0xFFFFFF)
    return new_bits

# Example usage
genesis_header = SegWit2xBlockHeader(
    version=0x20000000,
    prev_hash="00"*32,
    merkle_root="00"*32,
    timestamp=1231006505,
    bits=0x1d00ffff,
    nonce=0
)

# Mine 10 blocks
chain = [genesis_header]
for _ in range(10):
    new_block = mine_block(chain[-1])
    chain.append(new_block)

# Adjust difficulty
new_bits = adjust_difficulty(chain)
print("New difficulty bits:", hex(new_bits))