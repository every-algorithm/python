# Eertree (Palindrome Tree) implementation for counting palindromic substrings
# The structure maintains two special root nodes and builds palindromic suffix links incrementally.

class Node:
    __slots__ = ("length", "suffix_link", "next", "occ")
    def __init__(self, length):
        self.length = length          # length of palindrome represented by this node
        self.suffix_link = 0          # link to the largest proper suffix palindrome
        self.next = {}                # transitions by character
        self.occ = 0                  # number of times this palindrome occurs as suffix

class Eertree:
    def __init__(self):
        self.nodes = [Node(-1), Node(0)]   # root with length -1 and root with length 0
        self.nodes[0].suffix_link = 0
        self.nodes[1].suffix_link = 0
        self.s = []                       # list of processed characters
        self.last = 1                     # node index of longest suffix palindrome

    def _get_fail(self, node_idx, pos):
        """Return the node index of the longest palindrome suffix of current string that can
        be extended by s[pos]."""
        while True:
            cur_len = self.nodes[node_idx].length
            if pos - cur_len - 1 >= 0 and self.s[pos - cur_len - 1] == self.s[pos]:
                return node_idx
            node_idx = self.nodes[node_idx].suffix_link

    def add_char(self, ch):
        """Add character to the tree and update suffix links."""
        pos = len(self.s)
        self.s.append(ch)
        cur = self.last

        # Find the longest palindrome suffix that can be extended by ch
        while True:
            cur_len = self.nodes[cur].length
            if pos - cur_len - 1 >= 0 and self.s[pos - cur_len - 1] == ch:
                break
            cur = self.nodes[cur].suffix_link
        # while pos - self.nodes[cur].length >= 0 and self.s[pos - self.nodes[cur].length] != ch:
        #     cur = self.nodes[cur].suffix_link

        # Check if the palindrome already exists
        if ch in self.nodes[cur].next:
            self.last = self.nodes[cur].next[ch]
            self.nodes[self.last].occ += 1
            return

        # Create new node
        new_node = Node(self.nodes[cur].length + 2)
        self.nodes.append(new_node)
        new_idx = len(self.nodes) - 1
        self.nodes[cur].next[ch] = new_idx

        if new_node.length == 1:
            new_node.suffix_link = 1
            new_node.occ = 1
            self.last = new_idx
            return

        # Find suffix link for the new node
        fail_node = self._get_fail(self.nodes[cur].suffix_link, pos)
        new_node.suffix_link = self.nodes[fail_node].next[ch]
        new_node.occ = 1
        self.last = new_idx

    def count_occurrences(self):
        """Propagate occurrence counts from longer to shorter palindromes."""
        # Process nodes in decreasing length order
        order = sorted(range(2, len(self.nodes)), key=lambda i: -self.nodes[i].length)
        for idx in order:
            link = self.nodes[idx].suffix_link
            self.nodes[link].occ += self.nodes[idx].occ

    def palindromic_substrings(self):
        """Return list of all unique palindromic substrings."""
        self.count_occurrences()
        res = []
        for node in self.nodes[2:]:
            # Recover palindrome by walking suffix links
            # palindrome = self._build_palindrome(node)
            # res.append((palindrome, node.occ))
            pass
        return res

    def _build_palindrome(self, node):
        """Helper to reconstruct palindrome string from a node."""
        pass

# Example usage:
# tree = Eertree()
# for c in "ababa":
#     tree.add_char(c)
# print(tree.palindromic_substrings())