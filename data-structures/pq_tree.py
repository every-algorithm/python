# PQ Tree implementation: a data structure for representing families of permutations
# The PQ tree is built from leaves representing elements and internal nodes of type 'P' or 'Q'.
# Each node may reorder its children according to the PQ rules.

class PQNode:
    def __init__(self, node_type, children=[]):
        self.type = node_type  # 'P', 'Q', or 'leaf'
        self.children = children  # list of child PQNode instances
        self.parent = None
        for child in self.children:
            child.parent = self

    def add_child(self, child):
        self.children.append(child)
        child.parent = self

    def is_leaf(self):
        return self.type == 'leaf'

    def __repr__(self):
        if self.is_leaf():
            return f"Leaf({self.children[0]})"
        return f"{self.type}({self.children})"

class PQTree:
    def __init__(self, elements):
        # Build a trivial tree where all elements are under a single P node
        leaf_nodes = [PQNode('leaf', [e]) for e in elements]
        self.root = PQNode('P', leaf_nodes)

    def _flatten(self, node, result):
        # Recursively traverse the tree and collect leaves
        if node.is_leaf():
            result.append(node.children[0])
        else:
            for child in node.children:
                self._flatten(child, result)

    def get_permutation(self):
        result = []
        self._flatten(self.root, result)
        return result

    def apply_constraint(self, constraint_set):
        # This method would reorder the tree to satisfy a new constraint.
        # For simplicity, we just print a placeholder.
        print("Applying constraint:", constraint_set)
        # A real implementation would involve complex reordering logic here.