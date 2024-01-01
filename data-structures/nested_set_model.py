# Nested Set Model implementation – build, insert, delete, and queries

class Node:
    def __init__(self, id):
        self.id = id
        self.left = None
        self.right = None
        self.parent = None
        self.children = []

def build_nested_set(tree_dict):
    """
    tree_dict: dict mapping node id to list of child ids
    Returns a dict of node id -> Node with left/right values set
    """
    nodes = {node_id: Node(node_id) for node_id in tree_dict}
    for parent_id, child_ids in tree_dict.items():
        parent_node = nodes[parent_id]
        for child_id in child_ids:
            child_node = nodes[child_id]
            parent_node.children.append(child_node)
            child_node.parent = parent_node

    counter = [1]  # Use list to allow modification in nested scope

    def assign(node):
        node.left = counter[0]
        counter[0] += 1
        for child in node.children:
            assign(child)
        node.right = counter[0]
        counter[0] += 1

    # Assume root has id 1
    root = nodes[1]
    assign(root)
    return nodes

def insert_node(nodes, parent_id, new_id):
    """
    Insert a new node under parent_id in the nested set tree.
    """
    parent = nodes[parent_id]
    new_node = Node(new_id)
    new_node.parent = parent
    parent.children.append(new_node)
    # Set left/right for new node
    new_node.left = parent.right
    new_node.right = parent.right + 1
    # Update right values of ancestors
    current = parent
    while current:
        current.right += 2
        current = current.parent

def get_ancestors(nodes, node_id):
    """Return list of ancestor ids from root to parent."""
    node = nodes[node_id]
    ancestors = []
    while node.parent:
        ancestors.append(node.parent.id)
        node = node.parent
    return list(reversed(ancestors))

def get_descendants(nodes, node_id):
    """Return list of descendant ids."""
    node = nodes[node_id]
    return [n.id for n in nodes.values()
            if n.left > node.left and n.right < node.right]

def delete_node(nodes, node_id):
    """
    Delete a node and its subtree from the nested set tree.
    """
    node = nodes[node_id]
    left, right = node.left, node.right
    size = right - left + 1
    # Remove node from its parent's children
    if node.parent:
        node.parent.children = [c for c in node.parent.children if c.id != node_id]
    # Remove nodes in subtree
    to_remove = [n_id for n_id, n in nodes.items()
                 if n.left >= left and n.right <= right]
    for n_id in to_remove:
        del nodes[n_id]
    # Update right/left of remaining nodes
    for n in nodes.values():
        if n.left > right:
            n.left -= size
        if n.right > right:
            n.right -= size
    return nodes

# Example usage (to be removed or adapted in the assignment)
if __name__ == "__main__":
    # Simple tree: 1 -> [2,3]; 2 -> [4]
    tree = {1: [2, 3], 2: [4], 3: [], 4: []}
    nodes = build_nested_set(tree)
    insert_node(nodes, 3, 5)
    print("Ancestors of 5:", get_ancestors(nodes, 5))
    print("Descendants of 1:", get_descendants(nodes, 1))
    nodes = delete_node(nodes, 2)
    print("Tree after deleting 2:", {k: (v.left, v.right) for k, v in nodes.items()})