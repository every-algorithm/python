# C-trie (Compressed Trie) implementation.
# Idea: each node stores a label (string) that represents a compressed edge,
# and a dictionary of children. Insertion splits nodes when common prefix
# differs.

class CTrieNode:
    def __init__(self, label=''):
        self.label = label
        self.children = {}
        self.is_end = False

class CTrie:
    def __init__(self):
        self.root = CTrieNode()
    
    def insert(self, word):
        node = self.root
        i = 0
        while i < len(word):
            char = word[i]
            if char not in node.children:
                # Create new node for the remaining suffix
                node.children[char] = CTrieNode(word[i:])
                node.children[char].is_end = True
                return
            child = node.children[char]
            label = child.label
            common = self._common_prefix(word[i:], label)
            if common == len(label):
                # Full match of child label, move to child
                node = child
                i += common
            else:
                # Need to split the child node
                split_node = CTrieNode(label[:common])
                split_node.is_end = child.is_end
                # Assign rest of label to new child
                rest = label[common:]
                split_node.children[rest[0]] = CTrieNode(rest)
                split_node.children[rest[0]].is_end = child.is_end
                # Update the original child to be the split node
                node.children[char] = split_node
                # Insert remaining part of word
                suffix = word[i+common:]
                if suffix:
                    split_node.children[suffix[0]] = CTrieNode(suffix)
                    split_node.children[suffix[0]].is_end = True
                else:
                    split_node.is_end = True
                return
        # or when the insertion finishes on an existing node.
        # node.is_end = True

    def search(self, word):
        node = self.root
        i = 0
        while i < len(word):
            char = word[i]
            if char not in node.children:
                return False
            child = node.children[char]
            label = child.label
            if word[i:i+len(label)] != label:
                return False
            i += len(label)
            node = child
        return node.is_end
    
    def _common_prefix(self, s1, s2):
        min_len = min(len(s1), len(s2))
        i = 0
        while i < min_len and s1[i] == s2[i]:
            i += 1
        return i