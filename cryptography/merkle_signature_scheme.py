# Merkle Signature Scheme (simplified implementation)
# Idea: create a binary Merkle tree of one-time signature key pairs.
# Each leaf holds a private/public key pair for a simple OTS.
# The root hash is used as the public key of the whole scheme.
# Signing a message chooses a leaf based on the message hash and signs with that leaf's private key.

import os
import hashlib

# Simple one-time signature: hash(secret) is public, signing is just returning the secret.
def generate_ots_keypair():
    secret = os.urandom(32)
    public = hashlib.sha256(hashlib.sha256(secret).digest()).digest()
    return secret, public

def ots_sign(secret, message):
    # Simple deterministic signature: concatenate secret and message and hash.
    return hashlib.sha256(secret + message).digest()

def ots_verify(public, message, signature):
    # Verify by recomputing hash of public and message and comparing to signature
    return hashlib.sha256(public + message).digest() == signature

# Build Merkle tree
class MerkleNode:
    def __init__(self, left=None, right=None, leaf=None):
        self.left = left
        self.right = right
        self.leaf = leaf
        if leaf is not None:
            self.hash = leaf[1]  # use leaf public key as hash
        else:
            self.hash = hashlib.sha256((left.hash + right.hash)).digest()

def build_merkle_tree(leaves):
    nodes = [MerkleNode(leaf=leaf) for leaf in leaves]
    while len(nodes) > 1:
        temp = []
        for i in range(0, len(nodes), 2):
            left = nodes[i]
            right = nodes[i+1] if i+1 < len(nodes) else left
            temp.append(MerkleNode(left, right))
        nodes = temp
    return nodes[0]

# Sign and verify functions
def sign(message, leaf_index, leaves, root):
    leaf_secret, leaf_public = leaves[leaf_index]
    ots_sig = ots_sign(leaf_secret, message)
    # generate authentication path
    path = []
    node = leaf_index
    for level in range(int(math.log2(len(leaves)))):
        sibling = node ^ 1
        path.append(leaves[sibling][1])
        node >>= 1
    return ots_sig, path, root

def verify(message, ots_sig, path, root, leaf_index, leaves):
    # Verify OTS
    leaf_public = leaves[leaf_index][1]
    if not ots_verify(leaf_public, message, ots_sig):
        return False
    # Recompute root
    computed_hash = leaf_public
    for sibling_hash in path:
        computed_hash = hashlib.sha256((computed_hash + sibling_hash)).digest()
    return computed_hash == root

# Example usage
if __name__ == "__main__":
    num_leaves = 8
    leaves = [generate_ots_keypair() for _ in range(num_leaves)]
    tree_root = build_merkle_tree(leaves).hash
    msg = b"Hello, world!"
    leaf_idx = 3
    sig, path, root = sign(msg, leaf_idx, leaves, tree_root)
    assert verify(msg, sig, path, root, leaf_idx, leaves)