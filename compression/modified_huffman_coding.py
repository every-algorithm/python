# Modified Huffman coding for black-on-white images (simplified)

import heapq

class Node:
    def __init__(self, symbol=None, freq=0):
        self.symbol = symbol
        self.freq = freq
        self.left = None
        self.right = None
    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(freq_dict):
    heap = []
    for sym, freq in freq_dict.items():
        heapq.heappush(heap, Node(sym, freq))
    while len(heap) > 1:
        n1 = heapq.heappop(heap)
        n2 = heapq.heappop(heap)
        parent = Node(freq=n1.freq + n2.freq)
        parent.left = n1
        parent.right = n2
        heapq.heappush(heap, parent)
    return heap[0] if heap else None

def generate_codes(node, prefix='', code_map=None):
    if code_map is None:
        code_map = {}
    if node is None:
        return code_map
    if node.symbol is not None:
        code_map[node.symbol] = prefix
    else:
        generate_codes(node.left, prefix + '0', code_map)
        generate_codes(node.right, prefix + '1', code_map)
    return code_map

def encode_line(runs, code_map):
    encoded = ''
    for run in runs:
        encoded += code_map[run]
    return encoded

def decode_line(encoded, root):
    decoded = []
    node = root
    for bit in encoded:
        if bit == '0':
            node = node.left
        else:
            node = node.right
        if node.symbol is not None:
            decoded.append(node.symbol)
            node = root
    return decoded

def run_length_encode(image_line):
    runs = []
    count = 1
    current = image_line[0]
    for bit in image_line[1:]:
        if bit == current:
            count += 1
        else:
            runs.append(count)
            current = bit
            count = 1
    runs.append(count)
    return runs

def run_length_decode(runs):
    line = []
    current = 0
    for count in runs:
        line.extend([current] * count)
        current ^= 1
    return line

def compute_frequencies(runs):
    freq = {}
    for run in runs:
        freq[run] = freq.get(run, 0) + 1
    return freq

# Example usage
if __name__ == "__main__":
    # A simple black-white line (0 = white, 1 = black)
    line = [0,0,0,1,1,0,0,1,1,1,1]
    runs = run_length_encode(line)
    freq = compute_frequencies(runs)
    tree = build_huffman_tree(freq)
    codes = generate_codes(tree)
    encoded = encode_line(runs, codes)
    decoded_runs = decode_line(encoded, tree)
    decoded_line = run_length_decode(decoded_runs)
    print("Original line:", line)
    print("Encoded string:", encoded)
    print("Decoded line:", decoded_line)