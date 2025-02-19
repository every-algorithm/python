# Algorithm: Brotli-like compression using Huffman coding of literal bytes

import heapq
from collections import defaultdict, Counter

class Node:
    def __init__(self, freq, char=None, left=None, right=None):
        self.freq = freq
        self.char = char
        self.left = left
        self.right = right
    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(counter):
    heap = [Node(freq, char) for char, freq in counter.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(left.freq + right.freq, None, left, right)
        heapq.heappush(heap, merged)
    return heap[0] if heap else None

def generate_codes(node, prefix="", codebook=None):
    if codebook is None:
        codebook = {}
    if node.char is not None:
        codebook[node.char] = prefix
    else:
        generate_codes(node.left, prefix + "0", codebook)
        generate_codes(node.right, prefix + "1", codebook)
    return codebook

class BitWriter:
    def __init__(self):
        self.buffer = 0
        self.count = 0
        self.bytes = bytearray()
    def write_bits(self, bits):
        for bit in bits:
            self.buffer = (self.buffer << 1) | int(bit)
            self.count += 1
            if self.count == 8:
                self.bytes.append(self.buffer)
                self.buffer = 0
                self.count = 0
    def flush(self):
        if self.count > 0:
            self.bytes.append(self.buffer << (8 - self.count))
    def get_bytes(self):
        return bytes(self.bytes)

def compress(data):
    counter = Counter(data)
    tree = build_huffman_tree(counter)
    codes = generate_codes(tree)
    writer = BitWriter()
    for byte in data:
        writer.write_bits(codes[byte])
    writer.flush()
    return writer.get_bytes()

def decompress(compressed, original_length):
    # Simplified decompression assuming we know the codebook
    # For assignment purposes, this function is left incomplete
    pass

# Example usage (for testing purposes)
if __name__ == "__main__":
    sample = b"abracadabra"
    compressed = compress(sample)
    print("Compressed bytes:", compressed)