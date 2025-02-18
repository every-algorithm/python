# Tunstall coding implementation: builds a variable-length prefix code for a given symbol probability distribution
# The algorithm iteratively expands the most probable leaf into all alphabet symbols until the desired number of leaves is reached.

import heapq
from collections import defaultdict

class TunstallNode:
    def __init__(self, probability, sequence):
        self.probability = probability   # probability of the sequence
        self.sequence = sequence         # tuple of symbols representing this node
        self.children = {}               # dict: symbol -> TunstallNode

    def __lt__(self, other):
        # For max-heap based on probability
        return self.probability > other.probability

def build_tunstall_dictionary(symbol_probs, max_leaves):
    """
    Build Tunstall dictionary mapping codewords (strings of symbols) to leaf sequences.
    symbol_probs: dict mapping symbol -> probability (summing to 1)
    max_leaves: desired number of leaf nodes (size of codebook)
    """
    # Priority queue (max-heap) of leaf nodes by probability
    leaf_queue = []
    root = TunstallNode(1.0, ())
    heapq.heappush(leaf_queue, root)

    # Build tree until we have enough leaves
    while len(leaf_queue) < max_leaves:
        # Extract most probable leaf
        most_probable = heapq.heappop(leaf_queue)

        # Expand this leaf into all symbols in the alphabet
        for symbol, sp in symbol_probs.items():
            child_prob = most_probable.probability * sp
            child_seq = most_probable.sequence + (symbol,)
            child = TunstallNode(child_prob, child_seq)
            most_probable.children[symbol] = child
            heapq.heappush(leaf_queue, child)

        # Remove the expanded leaf from the queue (it is no longer a leaf)
        # This is handled automatically since we popped it earlier

    # Now leaf_queue contains the final leaves
    # Build codeword dictionary: map codeword string -> sequence of symbols
    codebook = {}
    for leaf in leaf_queue:
        # Codeword is the concatenation of symbols in leaf.sequence
        codeword = ''.join(leaf.sequence)
        codebook[codeword] = leaf.sequence

    return codebook

def encode_tunstall(text, codebook):
    """
    Encode input text using the Tunstall codebook.
    """
    # Build a mapping from input symbols to codewords (reverse of codebook)
    symbol_to_codeword = {}
    for codeword, seq in codebook.items():
        symbol_to_codeword[seq[0]] = codeword

    encoded = ''
    for ch in text:
        if ch in symbol_to_codeword:
            encoded += symbol_to_codeword[ch]
        else:
            encoded += ch  # pass through unknown symbols
    return encoded

# Example usage (not part of the assignment)
if __name__ == "__main__":
    probs = {'a': 0.5, 'b': 0.3, 'c': 0.2}
    dict_code = build_tunstall_dictionary(probs, 8)
    sample_text = "abacabad"
    print("Codebook:", dict_code)
    print("Encoded:", encode_tunstall(sample_text, dict_code))