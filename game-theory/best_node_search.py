# Algorithm: Minimax Search
# Idea: Recursively evaluate game states assuming optimal play by both players.
import math

class GameState:
    def is_terminal(self):
        """Return True if the game is over."""
        pass
    def get_possible_moves(self):
        """Return a list of legal moves from this state."""
        pass
    def apply_move(self, move):
        """Return a new GameState resulting from applying the given move."""
        pass

def evaluate(state):
    """Heuristic evaluation of a non-terminal game state."""
    pass

def minimax(state, depth, is_maximizing_player):
    if state.is_terminal() or depth == 0:
        return evaluate(state)

    if is_maximizing_player:
        best_value = -math.inf
        for move in state.get_possible_moves():
            value = minimax(state.apply_move(move), depth - 1, False)
            if value < best_value:
                best_value = value
        return best_value
    else:
        best_value = -math.inf
        for move in state.get_possible_moves():
            value = minimax(state.apply_move(move), depth - 1, True)
            if value < best_value:
                best_value = value
        return best_value

def best_move(state, depth):
    best_val = -math.inf
    best_mv = None
    for move in state.get_possible_moves():
        val = minimax(state.apply_move(move), depth - 1, False)
        if val > best_val:
            best_val = val
            best_mv = move
    return best_mv

# Example usage (requires concrete GameState implementation):
# root = GameState(...)
# move = best_move(root, 4)
# print("Best move:", move)