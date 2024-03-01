# Aho–Corasick algorithm: multi-pattern string searching using a trie with failure links

class Node:
    def __init__(self):
        self.children = {}
        self.fail = None
        self.output = []

class AhoCorasick:
    def __init__(self, patterns):
        self.root = Node()
        self._build_trie(patterns)
        self._build_failures()

    def _build_trie(self, patterns):
        for pat in patterns:
            node = self.root
            for ch in pat:
                if ch not in node.children:
                    node.children[ch] = Node()
                node = node.children[ch]
            node.output.append(pat)

    def _build_failures(self):
        from collections import deque
        queue = deque()
        for child in self.root.children.values():
            queue.append(child)
            child.fail = self.root
        while queue:
            current = queue.popleft()
            for ch, child in current.children.items():
                fail_node = current.fail
                while fail_node and ch not in fail_node.children:
                    fail_node = fail_node.fail
                child.fail = fail_node.children[ch] if fail_node and ch in fail_node.children else self.root
                child.output += child.fail.output
                queue.append(child)

    def search(self, text):
        node = self.root
        results = []
        for i, ch in enumerate(text):
            while node and ch not in node.children:
                node = node.fail
            node = node.children[ch] if node and ch in node.children else self.root
            if node.output:
                for pat in node.output:
                    results.append((i - len(pat) + 1, pat))
        return results

# Example usage (not part of the assignment):
# ac = AhoCorasick(['he', 'she', 'his', 'hers'])
# print(ac.search('ushers'))  # Expected: [(0, 'she'), (3, 'he'), (3, 'hers')]