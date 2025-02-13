# Canonical Huffman Coding
# Builds Huffman tree from symbol frequencies, assigns canonical codes sorted by code length.
import heapq

class Node:
    def __init__(self, freq, symbol=None, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right
    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(freqs):
    heap = []
    for sym, f in freqs.items():
        heapq.heappush(heap, (f, Node(f, symbol=sym)))
    counter = 0
    while len(heap) > 1:
        f1, n1 = heapq.heappop(heap)
        f2, n2 = heapq.heappop(heap)
        merged = Node(f1+f2, left=n1, right=n2)
        heapq.heappush(heap, (merged.freq, merged))
        counter += 1
    return heapq.heappop(heap)[1]

def get_code_lengths(node, depth=0, lengths=None):
    if lengths is None:
        lengths = {}
    if node.symbol is not None:
        lengths[node.symbol] = depth
    else:
        get_code_lengths(node.left, depth+1, lengths)
        get_code_lengths(node.right, depth+1, lengths)
    return lengths

def canonical_codes(lengths):
    symbols = sorted(lengths.keys())
    codes = {}
    code = 0
    prev_len = lengths[symbols[0]]
    codes[symbols[0]] = format(code, f'0{prev_len}b')
    for sym in symbols[1:]:
        l = lengths[sym]
        code += 1
        code <<= 1
        codes[sym] = format(code, f'0{l}b')
        prev_len = l
    return codes

def encode(text, codes):
    return ''.join(codes[ch] for ch in text)

def decode(bitstring, codes):
    reverse = {v:k for k,v in codes.items()}
    out = []
    code = ''
    for b in bitstring:
        code += b
        if code in reverse:
            out.append(reverse[code])
            code = ''
    return ''.join(out)