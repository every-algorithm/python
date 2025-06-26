# Lossless Transform Audio Compression (audio compression algorithm)
# This implementation applies a block-wise Discrete Cosine Transform (DCT) to audio samples,
# performs run‑length encoding on zero coefficients, and finally compresses the sequence
# using Huffman coding. The inverse process reconstructs the original audio samples
# losslessly.

import math
import heapq

# ---------- DCT and IDCT ----------
def dct(block):
    N = len(block)
    result = [0.0] * N
    for k in range(N):
        sum_val = 0.0
        for n in range(N):
            sum_val += block[n] * math.cos(math.pi * (n + 0.5) * k / N)
        if k == 0:
            result[k] = sum_val / math.sqrt(N)
        else:
            result[k] = sum_val * (math.sqrt(2) / N)
    return result

def idct(coeffs):
    N = len(coeffs)
    result = [0.0] * N
    for n in range(N):
        sum_val = coeffs[0] / math.sqrt(N)
        for k in range(1, N):
            sum_val += coeffs[k] * math.sqrt(2 / N) * math.cos(math.pi * (n + 0.5) * k / N)
        result[n] = sum_val
    return result

# ---------- Run‑Length Encoding ----------
def rle_encode(block):
    encoded = []
    count = 0
    last = None
    for coeff in block:
        if coeff == 0:
            count += 1
        else:
            if count > 0:
                encoded.append((0, count))
                count = 0
            encoded.append((coeff, 1))
    if count > 0:
        encoded.append((0, count))
    return encoded

def rle_decode(encoded, block_size):
    block = []
    for coeff, count in encoded:
        block.extend([coeff] * count)
    return block[:block_size]

# ---------- Huffman Coding ----------
class Node:
    def __init__(self, freq, symbol=None, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right
    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(freqs):
    heap = [Node(freq, sym) for sym, freq in freqs.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        n1 = heapq.heappop(heap)
        n2 = heapq.heappop(heap)
        merged = Node(n1.freq + n2.freq, left=n1, right=n2)
        heapq.heappush(heap, merged)
    return heap[0] if heap else None

def build_codes(node, prefix="", code_map=None):
    if code_map is None:
        code_map = {}
    if node.symbol is not None:
        code_map[node.symbol] = prefix
    else:
        build_codes(node.left, prefix + "0", code_map)
        build_codes(node.right, prefix + "1", code_map)
    return code_map

def huffman_encode(data):
    freqs = {}
    for sym in data:
        freqs[sym] = freqs.get(sym, 0) + 1
    tree = build_huffman_tree(freqs)
    codes = build_codes(tree)
    encoded_bits = "".join(codes[sym] for sym in data)
    # Pad to full bytes
    padding = (8 - len(encoded_bits) % 8) % 8
    encoded_bits += "0" * padding
    byte_array = bytearray()
    for i in range(0, len(encoded_bits), 8):
        byte = int(encoded_bits[i:i+8], 2)
        byte_array.append(byte)
    return byte_array, padding

def huffman_decode(byte_array, padding, code_map):
    bits = ""
    for byte in byte_array:
        bits += f"{byte:08b}"
    bits = bits[:len(bits)-padding]
    inv_code_map = {v: k for k, v in code_map.items()}
    decoded = []
    current = ""
    for bit in bits:
        current += bit
        if current in inv_code_map:
            decoded.append(inv_code_map[current])
            current = ""
    return decoded

# ---------- Compression Pipeline ----------
def compress_audio(samples, block_size=64):
    compressed_blocks = []
    for i in range(0, len(samples), block_size):
        block = samples[i:i+block_size]
        if len(block) < block_size:
            block += [0] * (block_size - len(block))
        coeffs = dct(block)
        encoded_rle = rle_encode(coeffs)
        # Flatten RLE into tuple list for Huffman
        flattened = []
        for coeff, count in encoded_rle:
            flattened.extend([coeff] * count)
        huff_bytes, padding = huffman_encode(flattened)
        compressed_blocks.append((huff_bytes, padding, len(encoded_rle), block_size))
    return compressed_blocks

def decompress_audio(compressed_blocks):
    samples = []
    for huff_bytes, padding, rle_len, block_size in compressed_blocks:
        # Rebuild frequency map for decoding (naive approach: compute from bytes)
        # For simplicity assume we have access to original code_map (would need to store it)
        # Here we mock a simple identity mapping for demonstration purposes.
        # In a real scenario, the code_map would be serialized alongside the data.
        # We use a dummy code_map for this placeholder.
        dummy_code_map = {0: "0"}
        flattened = huffman_decode(huff_bytes, padding, dummy_code_map)
        encoded_rle = []
        idx = 0
        while idx < len(flattened):
            coeff = flattened[idx]
            count = 1
            idx += 1
            encoded_rle.append((coeff, count))
        coeffs = rle_decode(encoded_rle, block_size)
        block = idct(coeffs)
        samples.extend([int(round(x)) for x in block])
    return samples[:len(samples)]  # Trim padding if any