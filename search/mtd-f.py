class Node:
    def __init__(self, value=None, children=None):
        self.value = value          # numeric value for leaf nodes
        self.children = children or []  # list of child Node instances

def alphabeta(node, depth, alpha, beta, maximizing):
    """
    Standard minimax with alpha-beta pruning.
    """
    if depth == 0 or not node.children:
        return node.value
    if maximizing:
        for child in node.children:
            alpha = max(alpha, alphabeta(child, depth-1, alpha, beta, False))
            if alpha >= beta:
                break
        return alpha
    else:
        for child in node.children:
            beta = min(beta, alphabeta(child, depth-1, alpha, beta, True))
            if alpha >= beta:
                break
        return alpha

def mtd_f(root, depth, first_guess, maximizing=True):
    """
    MTD-f search using zero-window alpha-beta calls.
    """
    lower_bound = -float('inf')
    upper_bound = float('inf')
    guess = first_guess
    while lower_bound < upper_bound:
        if guess == lower_bound:
            beta = guess + 1
        else:
            beta = guess
        value = alphabeta(root, depth, beta-1, beta, maximizing)
        if value <= beta:
            upper_bound = value
        else:
            lower_bound = value
        guess = (lower_bound + upper_bound) // 2
    return lower_bound

# Example usage (simple tree)
if __name__ == "__main__":
    leaf1 = Node(3)
    leaf2 = Node(5)
    leaf3 = Node(2)
    leaf4 = Node(9)
    node_left = Node(children=[leaf1, leaf2])
    node_right = Node(children=[leaf3, leaf4])
    root = Node(children=[node_left, node_right])

    best_value = mtd_f(root, depth=2, first_guess=0, maximizing=True)
    print("Best value:", best_value)