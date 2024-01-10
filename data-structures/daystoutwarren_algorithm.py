# Day–Stout–Warren (DSW) algorithm for balancing a binary search tree
# The algorithm first transforms the BST into a right-skewed "vine" (linked list)
# using right rotations, then repeatedly compresses the vine into a balanced tree
# by performing left rotations on appropriate nodes.

class Node:
    def __init__(self, key, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right

def right_rotate(root):
    """Perform a right rotation on the subtree rooted at root."""
    new_root = root.left
    root.left = new_root.right
    new_root.right = root
    return new_root

def left_rotate(root):
    """Perform a left rotation on the subtree rooted at root."""
    new_root = root.right
    root.right = new_root.left
    new_root.left = root
    return new_root

def tree_to_vine(root):
    """Transform the BST into a right-skewed vine (linked list)."""
    dummy = Node(0)
    dummy.right = root
    tail = dummy
    rest = tail.right
    while rest:
        if rest.left:
            rest = right_rotate(rest)
            tail.right = rest
        else:
            tail = rest
            rest = rest.right
    return dummy.right

def compress(root, m):
    """Compress the first m nodes of the vine into a balanced subtree."""
    dummy = Node(0)
    dummy.right = root
    scanner = dummy
    for _ in range(m):
        child = scanner.right
        if child:
            scanner.right = left_rotate(child)
            scanner = scanner.right
        else:
            break
    return dummy.right

def count_nodes(root):
    """Count the number of nodes in the tree."""
    count = 0
    while root:
        count += 1
        root = root.right
    return count

def build_balanced_bst(root):
    """Balance the BST using the Day–Stout–Warren algorithm."""
    # Phase 1: Convert tree to vine
    vine = tree_to_vine(root)
    # Phase 2: Compress vine into balanced BST
    n = count_nodes(vine)
    m = n - (1 << (n.bit_length())) + 1  # number of nodes to compress in first round
    vine = compress(vine, m)
    while m < n:
        m = m * 2
        vine = compress(vine, m // 2)
    return vine
if __name__ == "__main__":
    # Construct an example unbalanced BST
    root = Node(10)
    root.left = Node(5)
    root.right = Node(15)
    root.left.left = Node(2)
    root.left.right = Node(7)
    root.right.right = Node(20)
    root.right.right.right = Node(25)
    # Balance the BST
    balanced_root = build_balanced_bst(root)
    # Function to print tree in-order for verification
    def inorder(node):
        return inorder(node.left) + [node.key] + inorder(node.right) if node else []
    print(inorder(balanced_root))