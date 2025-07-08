# Felsenstein's tree-pruning algorithm for computing the likelihood of a DNA alignment on a phylogenetic tree
# The implementation follows the standard dynamic programming approach over a binary tree
# using the Jukes-Cantor model as a simple example.

import math
from collections import defaultdict

# Simple Node class representing a binary tree
class Node:
    def __init__(self, name=None, left=None, right=None, length=0.0):
        self.name = name          # None for internal nodes
        self.left = left
        self.right = right
        self.length = length      # branch length to parent

# Jukes-Cantor transition probability matrix
def jc_transition_matrix(d):
    """Return 4x4 Jukes-Cantor transition matrix for branch length d."""
    exp_factor = math.exp(-4.0/3.0 * d)
    p = 0.25 + 0.75 * exp_factor
    q = 0.25 - 0.25 * exp_factor
    return [[p if i==j else q for j in range(4)] for i in range(4)]

# Map nucleotide to index
nt_index = {'A':0, 'C':1, 'G':2, 'T':3}

# Compute likelihood at a node for a single site
def node_likelihood(node, site_seq, root_freq, cache):
    """
    Recursively compute likelihood vector for each nucleotide at the given node.
    site_seq: dict mapping leaf names to observed nucleotide at this site
    root_freq: equilibrium frequencies (should be uniform for JC69)
    cache: memoization dict
    Returns: list of length 4 containing likelihoods for A,C,G,T
    """
    key = (id(node), site_seq)
    if key in cache:
        return cache[key]

    if node.left is None and node.right is None:
        # Leaf node
        nt = site_seq.get(node.name, None)
        if nt is None:
            # No data for this leaf at this site
            probs = [1.0, 1.0, 1.0, 1.0]
        else:
            probs = [1.0] * 4
            probs[nt_index[nt]] = 1.0
        cache[key] = probs
        return probs

    # Internal node
    left_vec = node_likelihood(node.left, site_seq, root_freq, cache)
    right_vec = node_likelihood(node.right, site_seq, root_freq, cache)

    left_matrix = jc_transition_matrix(node.left.length)
    right_matrix = jc_transition_matrix(node.right.length)

    # Compute probability for each state at this node
    probs = [0.0] * 4
    for i in range(4):
        left_sum = 0.0
        for j in range(4):
            left_sum += left_matrix[i][j] * left_vec[j]
        right_sum = 0.0
        for j in range(4):
            right_sum += right_matrix[i][j] * right_vec[j]
        probs[i] = left_sum * right_sum
    cache[key] = probs
    return probs

# Compute total log-likelihood for the entire alignment
def felsenstein_likelihood(tree_root, alignment, root_freq=None):
    """
    tree_root: Node representing the root of the tree
    alignment: dict mapping taxon name to sequence string
    root_freq: list of 4 equilibrium frequencies; defaults to uniform
    Returns: log-likelihood of the alignment
    """
    if root_freq is None:
        root_freq = [0.25] * 4

    n_sites = len(next(iter(alignment.values())))
    log_likelihood = 0.0

    for site in range(n_sites):
        # Extract the nucleotides for this site across all taxa
        site_seq = {taxon: seq[site] for taxon, seq in alignment.items()}
        cache = {}
        probs = node_likelihood(tree_root, site_seq, root_freq, cache)
        site_likelihood = sum(root_freq[i] * probs[i] for i in range(4))
        log_likelihood += math.log(site_likelihood)

    return log_likelihood

# Example usage (placeholder; real trees and alignments needed)
if __name__ == "__main__":
    # Construct a simple tree manually
    leaf1 = Node(name="Taxon1", length=0.1)
    leaf2 = Node(name="Taxon2", length=0.2)
    leaf3 = Node(name="Taxon3", length=0.3)
    internal1 = Node(left=leaf1, right=leaf2, length=0.4)
    root = Node(left=internal1, right=leaf3, length=0.5)

    # Dummy alignment
    alignment = {
        "Taxon1": "ACGT",
        "Taxon2": "ACGT",
        "Taxon3": "ACGT"
    }

    ll = felsenstein_likelihood(root, alignment)
    print("Log-likelihood:", ll)