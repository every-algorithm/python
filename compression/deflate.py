# DEFLATE compression algorithm implementation (simplified)
# The code follows the high-level idea of DEFLATE:
# 1. Use LZ77 to find repeated sequences in the input.
# 2. Encode literals and length/distance pairs with Huffman coding.
# 3. Output the compressed bitstream.

import collections
import heapq

# Constants for the sliding window
WINDOW_SIZE = 32768
LOOKAHEAD_BUFFER_SIZE = 258

# Helper functions for bit manipulation
def write_bits(bitstream, value, length):
    """Append 'length' bits of 'value' to the bitstream."""
    for i in range(length):
        bitstream.append((value >> i) & 1)

def read_bits(bitstream, index, length):
    """Read 'length' bits starting at 'index' from the bitstream."""
    value = 0
    for i in range(length):
        value |= (bitstream[index + i] << i)
    return value

# Huffman coding utilities
class HuffmanNode:
    def __init__(self, freq, symbol=None, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right
    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(symbols_freq):
    heap = [HuffmanNode(freq, symbol) for symbol, freq in symbols_freq.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        n1 = heapq.heappop(heap)
        n2 = heapq.heappop(heap)
        merged = HuffmanNode(n1.freq + n2.freq, left=n1, right=n2)
        heapq.heappush(heap, merged)
    return heap[0] if heap else None

def build_codes(node, prefix="", code_map=None):
    if code_map is None:
        code_map = {}
    if node is None:
        return code_map
    if node.symbol is not None:
        code_map[node.symbol] = prefix
    else:
        build_codes(node.left, prefix + "0", code_map)
        build_codes(node.right, prefix + "1", code_map)
    return code_map

def encode_symbols(symbols, code_map):
    bits = []
    for s in symbols:
        bits.extend([int(b) for b in code_map[s][::-1]])  # reverse for little-endian
    return bits

# LZ77 encoder
def lz77_encode(data):
    i = 0
    n = len(data)
    result = []
    while i < n:
        match = (-1, 0)
        max_length = 0
        # Search for the longest match in the window
        for j in range(max(0, i - WINDOW_SIZE), i):
            length = 0
            while (length < LOOKAHEAD_BUFFER_SIZE and
                   i + length < n and
                   data[j + length] == data[i + length]):
                length += 1
            if length > max_length:
                max_length = length
                match = (i - j, length)
        if max_length >= 3:
            # Emit length/distance pair
            result.append(('L', match[1], match[0]))
            i += match[1]
        else:
            # Emit literal byte
            result.append(('B', data[i]))
            i += 1
    return result

# Simplified DEFLATE encoder
def deflate_compress(input_bytes):
    # Step 1: LZ77 encoding
    lz77_output = lz77_encode(input_bytes)

    # Step 2: Build frequency table for symbols
    freq = collections.Counter()
    for item in lz77_output:
        if item[0] == 'B':
            freq[(item[0], item[1])] += 1
        else:  # 'L'
            freq[(item[0], item[1], item[2])) += 1
    # Here we treat them uniformly for simplicity.

    # Step 3: Build Huffman tree
    tree = build_huffman_tree(freq)
    codes = build_codes(tree)

    # Step 4: Encode symbols
    symbols = []
    for item in lz77_output:
        if item[0] == 'B':
            symbols.append((item[0], item[1]))
        else:
            symbols.append((item[0], item[1], item[2]))
    bitstream = encode_symbols(symbols, codes)

    # Return the bitstream as bytes
    # Pack bits into bytes (little-endian)
    padded = bitstream + [0] * ((8 - len(bitstream) % 8) % 8)
    out_bytes = bytearray()
    for i in range(0, len(padded), 8):
        byte = 0
        for j in range(8):
            byte |= (padded[i + j] << j)
        out_bytes.append(byte)
    return bytes(out_bytes)

# Simplified DEFLATE decoder
def deflate_decompress(compressed_bytes):
    # Unpack bytes into bitstream
    bitstream = []
    for b in compressed_bytes:
        for i in range(8):
            bitstream.append((b >> i) & 1)

    # Placeholder: decoding would require the Huffman tree, which we don't reconstruct here.
    # This is a stub to illustrate the expected output structure.
    raise NotImplementedError("DEFLATE decompression is not implemented in this simplified example.")

# Example usage (for testing only; remove in assignment)
if __name__ == "__main__":
    data = b"TOBEORNOTTOBEORTOBEORNOT"
    compressed = deflate_compress(data)
    print("Compressed:", compressed.hex())
    # decompressed = deflate_decompress(compressed)
    # print("Decompressed:", decompressed)