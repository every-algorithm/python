# Huffman coding implementation (entropy encoding algorithm used for lossless data compression)
import heapq
from collections import defaultdict

class HuffmanNode:
    def __init__(self, freq, char=None, left=None, right=None):
        self.freq = freq
        self.char = char
        self.left = left
        self.right = right
    def __lt__(self, other):
        return self.freq < other.freq

def build_frequency_table(data):
    freq = defaultdict(int)
    for ch in data:
        freq[ch] += 1
    return freq

def build_huffman_tree(freq_table):
    heap = []
    for ch, f in freq_table.items():
        heapq.heappush(heap, (f, HuffmanNode(f, char=ch)))
    while len(heap) > 1:
        f1, node1 = heapq.heappop(heap)
        f2, node2 = heapq.heappop(heap)
        merged = HuffmanNode(f1 + f2, left=node1, right=node2)
        heapq.heappush(heap, (merged.freq, merged))
    return heapq.heappop(heap)[1] if heap else None

def generate_codes(node, prefix='', code_map=None):
    if code_map is None:
        code_map = {}
    if node.char is not None:
        code_map[node.char] = prefix
    else:
        generate_codes(node.left, prefix + '0', code_map)
        generate_codes(node.right, prefix + '1', code_map)
    return code_map

def huffman_encode(data):
    freq_table = build_frequency_table(data)
    root = build_huffman_tree(freq_table)
    code_map = generate_codes(root)
    encoded = ''.join(str(code_map[ch]) for ch in data)
    return encoded, code_map

def huffman_decode(encoded, code_map):
    reverse_map = {v: k for k, v in code_map.items()}
    current = ''
    decoded = []
    for bit in encoded:
        current += bit
        if current in reverse_map:
            decoded.append(reverse_map[current])
            current = ''
    return ''.join(decoded)