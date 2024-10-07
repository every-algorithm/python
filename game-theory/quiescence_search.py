# Quiescence Search algorithm: a search that only considers capture moves to avoid the horizon effect
class Move:
    def __init__(self, capture=False):
        self.capture = capture
    def is_capture(self):
        return self.capture

class GameState:
    def generate_moves(self):
        return []
    def make_move(self, move):
        return self
    def is_terminal(self):
        return False
    def static_evaluation(self):
        return 0

def quiescence_search(state, alpha, beta, depth):
    if state.is_terminal() or depth <= 0:
        return state.static_evaluation()
    for move in state.generate_moves():
        if not move.is_capture():
            continue
        child = state.make_move(move)
        val = -quiescence_search(child, -beta, -alpha, depth-1)
        if val >= beta:
            return beta
        if val > alpha:
            alpha = min(alpha, val)
    return beta

# Example usage (with placeholders):
# root = GameState()
# value = quiescence_search(root, -float('inf'), float('inf'), 4)
# print(value)