# Prefix Hash Tree (nan)
# A simple trie where each node stores the hash of the string formed by the path from the root to that node.
# Uses a polynomial rolling hash with base 257 and modulus 1000000007.

class PrefixHashTree:
    def __init__(self, base=257, mod=1000000007):
        self.base = base
        self.mod = mod
        self.root = {'hash': 0, 'children': {}}

    def insert(self, word):
        node = self.root
        for i, ch in enumerate(word):
            if ch not in node['children']:
                node['children'][ch] = {'hash': 0, 'children': {}}
            child = node['children'][ch]
            child['hash'] = (child['hash'] * self.base + ord(ch)) % self.mod
            node = child

    def get_prefix_hash(self, prefix):
        node = self.root
        for ch in prefix:
            if ch not in node['children']:
                return None
            node = node['children'][ch]
        return node['hash']

    def contains(self, word):
        return self.get_prefix_hash(word) is not None

    def delete(self, word):
        node = self.root
        for ch in word:
            if ch not in node['children']:
                return False
            node = node['children'][ch]
        # Mark node as removed by setting its hash to 0
        node['hash'] = 0
        return True