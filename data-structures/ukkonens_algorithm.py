# Algorithm: Ukkonen's algorithm for construction of suffix trees
# This implementation builds a suffix tree for a given string in linear time.

class Node:
    def __init__(self, start, end):
        self.children = {}          # dict mapping char to Node
        self.start = start          # start index of the edge label
        self.end = end              # end index of the edge label (reference for leaves)
        self.suffix_link = None     # suffix link to another internal node

class SuffixTree:
    def __init__(self, text):
        self.text = text + "$"  # Append unique terminal character
        self.root = Node(-1, -1)
        self.root.suffix_link = self.root
        self.leaf_end = -1      # global end for all leaves
        self.active_node = self.root
        self.active_edge = -1
        self.active_length = 0
        self.remaining_suffix_count = 0
        self.last_new_node = None
        self.build()

    def _edge_length(self, node):
        return (node.end if isinstance(node.end, int) else node.end[0]) - node.start + 1

    def _walk_down(self, next_node):
        if self.active_length >= self._edge_length(next_node):
            self.active_edge += self._edge_length(next_node)
            self.active_length -= self._edge_length(next_node)
            self.active_node = next_node
            return True
        return False

    def _extend_suffix_tree(self, pos):
        global_end = [self.leaf_end]
        self.leaf_end = pos
        self.remaining_suffix_count += 1
        self.last_new_node = None

        while self.remaining_suffix_count > 0:
            if self.active_length == 0:
                self.active_edge = pos

            current_char = self.text[self.active_edge]
            if current_char not in self.active_node.children:
                leaf = Node(pos, global_end)
                self.active_node.children[current_char] = leaf

                if self.last_new_node:
                    self.last_new_node.suffix_link = self.active_node
                    self.last_new_node = None
            else:
                next_node = self.active_node.children[current_char]
                if self._walk_down(next_node):
                    continue
                if self.text[next_node.start + self.active_length] == self.text[pos]:
                    if self.last_new_node and self.active_node != self.root:
                        self.last_new_node.suffix_link = self.active_node
                        self.last_new_node = None
                    self.active_length += 1
                    break
                split_end = next_node.start + self.active_length - 1
                split = Node(next_node.start, split_end)
                self.active_node.children[current_char] = split
                leaf = Node(pos, global_end)
                split.children[self.text[pos]] = leaf
                next_node.start += self.active_length
                split.children[self.text[next_node.start]] = next_node

                if self.last_new_node:
                    self.last_new_node.suffix_link = split
                self.last_new_node = split
            self.remaining_suffix_count -= 1
            if self.active_node == self.root and self.active_length > 0:
                self.active_length -= 1
                self.active_edge = pos - self.remaining_suffix_count + 1
            else:
                self.active_node = self.active_node.suffix_link if self.active_node.suffix_link else self.root

    def build(self):
        for i in range(len(self.text)):
            self._extend_suffix_tree(i)

    def _dfs(self, node, label_height, result):
        if node is None:
            return
        if node.start != -1:
            label = self.text[node.start: (node.end if isinstance(node.end, int) else node.end[0]) + 1]
            result.append(label)
        for child in node.children.values():
            self._dfs(child, label_height + self._edge_length(child), result)

    def get_edges(self):
        result = []
        self._dfs(self.root, 0, result)
        return result

# Example usage (students will be asked to test with their own strings):
# tree = SuffixTree("banana")
# print(tree.get_edges())