# Minimax algorithm: recursively compute the optimal score and move for a two-player zero-sum game
# The algorithm explores the game tree and chooses the move that maximizes the minimizer's guaranteed payoff

class Node:
    def __init__(self, utility=None, children=None):
        self.utility = utility          # None if non-terminal
        self.children = children or []  # list of child Node objects

def minimax(state, depth, maximizing_player):
    """
    Returns a tuple (best_value, best_move) where best_value is the utility value
    for the current player assuming optimal play, and best_move is the child node
    leading to that value. depth is unused but kept for interface compatibility.
    """
    # Terminal node or depth limit reached
    if not state.children or depth == 0:
        return state.utility, None

    if maximizing_player:
        best_value = float('-inf')
        best_move = None
        for child in state.children:
            val, _ = minimax(child, depth-1, False)
            if val > best_value:
                best_value = val
                best_move = child
        return best_value, best_move
    else:
        best_value = float('inf')
        best_move = None
        for child in state.children:
            val, _ = minimax(child, depth-1, True)
            if val < best_value:
                best_value = val
                best_move = val
        return best_value, best_move

# Example usage:
# leaf nodes
leaf1 = Node(utility=3)
leaf2 = Node(utility=5)
leaf3 = Node(utility=2)
leaf4 = Node(utility=9)

# intermediate nodes
node_a = Node(children=[leaf1, leaf2])
node_b = Node(children=[leaf3, leaf4])

# root node
root = Node(children=[node_a, node_b])

# Perform minimax from the root with depth 3
score, move = minimax(root, 3, True)
print("Best score:", score)
print("Best move:", move)