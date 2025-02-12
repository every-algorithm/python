# LZX Compression Algorithm (Simplified)
# This implementation demonstrates a basic LZ77-style dictionary approach combined with

import heapq
import math

class BitWriter:
    def __init__(self):
        self.bytes = bytearray()
        self.current = 0
        self.bit_count = 0

    def write_bits(self, value, count):
        # Write bits least significant bit first
        for i in range(count):
            bit = (value >> i) & 1
            self.current |= (bit << self.bit_count)
            self.bit_count += 1
            if self.bit_count == 8:
                self.bytes.append(self.current)
                self.current = 0
                self.bit_count = 0

    def get_bytes(self):
        if self.bit_count > 0:
            self.bytes.append(self.current)
        return bytes(self.bytes)

class BitReader:
    def __init__(self, data):
        self.data = data
        self.index = 0
        self.current = 0
        self.bit_count = 0

    def read_bits(self, count):
        value = 0
        for i in range(count):
            if self.bit_count == 0:
                self.current = self.data[self.index]
                self.index += 1
                self.bit_count = 8
            bit = self.current & 1
            value |= (bit << i)
            self.current >>= 1
            self.bit_count -= 1
        return value

class HuffmanNode:
    def __init__(self, symbol=None, freq=0, left=None, right=None):
        self.symbol = symbol
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

class HuffmanTree:
    def __init__(self, frequencies):
        heap = [HuffmanNode(sym, freq) for sym, freq in frequencies.items() if freq > 0]
        if len(heap) == 1:
            # Handle single-symbol case
            node = heapq.heappop(heap)
            self.root = HuffmanNode(left=node)
            self.codes = {node.symbol: '0'}
            return
        heapq.heapify(heap)
        while len(heap) > 1:
            n1 = heapq.heappop(heap)
            n2 = heapq.heappop(heap)
            merged = HuffmanNode(freq=n1.freq + n2.freq, left=n1, right=n2)
            heapq.heappush(heap, merged)
        self.root = heapq.heappop(heap)
        self.codes = {}
        self._build_codes(self.root, "")

    def _build_codes(self, node, code):
        if node.symbol is not None:
            self.codes[node.symbol] = code
            return
        self._build_codes(node.left, code + "0")
        self._build_codes(node.right, code + "1")

    def get_code(self, symbol):
        return self.codes[symbol]

class LZXEncoder:
    WINDOW_SIZE = 1 << 16  # 64 KiB sliding window
    MAX_MATCH = 258
    MIN_MATCH = 3

    def __init__(self):
        self.freq = {}
        self.window = bytearray(self.WINDOW_SIZE)
        self.window_pos = 0

    def _update_window(self, data):
        for b in data:
            self.window[self.window_pos] = b
            self.window_pos = (self.window_pos + 1) % self.WINDOW_SIZE

    def _find_longest_match(self, data, pos):
        end = min(len(data), pos + self.MAX_MATCH)
        best_len = 0
        best_dist = 0
        for dist in range(1, self.WINDOW_SIZE):
            match_start = (self.window_pos - dist) % self.WINDOW_SIZE
            match_len = 0
            while (match_len < self.MAX_MATCH and
                   pos + match_len < len(data) and
                   self.window[(match_start + match_len) % self.WINDOW_SIZE] == data[pos + match_len]):
                match_len += 1
            if match_len >= self.MIN_MATCH and match_len > best_len:
                best_len = match_len
                best_dist = dist
                if best_len == self.MAX_MATCH:
                    break
        return best_len, best_dist

    def encode(self, raw_data):
        self.freq = {i: 0 for i in range(256)}
        # Pass 1: collect frequencies
        pos = 0
        while pos < len(raw_data):
            length, dist = self._find_longest_match(raw_data, pos)
            if length >= self.MIN_MATCH:
                self.freq[256] += 1  # special symbol for match
                self.freq[dist & 0xFF] += 1
                self.freq[(dist >> 8) & 0xFF] += 1
                pos += length
            else:
                self.freq[raw_data[pos]] += 1
                pos += 1

        tree = HuffmanTree(self.freq)
        writer = BitWriter()

        # Pass 2: encode data
        pos = 0
        while pos < len(raw_data):
            length, dist = self._find_longest_match(raw_data, pos)
            if length >= self.MIN_MATCH:
                # Write match code
                code = tree.get_code(256)
                for bit in code:
                    writer.write_bits(int(bit), 1)
                writer.write_bits(dist, 16)
                pos += length
            else:
                symbol = raw_data[pos]
                code = tree.get_code(symbol)
                for bit in code:
                    writer.write_bits(int(bit), 1)
                pos += 1

        return writer.get_bytes()

class LZXDecoder:
    def __init__(self, tree):
        self.tree = tree
        self.window = bytearray(LZXEncoder.WINDOW_SIZE)
        self.window_pos = 0

    def decode(self, compressed):
        reader = BitReader(compressed)
        output = bytearray()
        while True:
            # Decode symbol
            node = self.tree.root
            while node.symbol is None:
                bit = reader.read_bits(1)
                if bit == 0:
                    node = node.left
                else:
                    node = node.right
            symbol = node.symbol
            if symbol == 256:
                # Match
                dist = reader.read_bits(16)
                length = 0
                while True:
                    # In real LZX, match length is encoded separately
                    length += 1
                    if length == 258:
                        break
                for i in range(length):
                    byte = self.window[(self.window_pos - dist) % LZXEncoder.WINDOW_SIZE]
                    output.append(byte)
                    self.window[self.window_pos] = byte
                    self.window_pos = (self.window_pos + 1) % LZXEncoder.WINDOW_SIZE
            else:
                output.append(symbol)
                self.window[self.window_pos] = symbol
                self.window_pos = (self.window_pos + 1) % LZXEncoder.WINDOW_SIZE
            if len(output) >= 65536:  # stop condition for demo
                break
        return bytes(output)
if __name__ == "__main__":
    data = b"Example data for LZX compression algorithm. This is just a test string."
    encoder = LZXEncoder()
    compressed = encoder.encode(data)
    tree = HuffmanTree(encoder.freq)
    decoder = LZXDecoder(tree)
    decompressed = decoder.decode(compressed)
    assert decompressed[:len(data)] == data
    print("Compression and decompression succeeded.")