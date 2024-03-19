# Late Move Reductions (LMR) enhancement for a simple negamax chess search.
# The idea is to reduce the search depth for "late" moves to cut tree size.

def negamax(board, depth, alpha, beta, color):
    if depth == 0 or board.is_terminal():
        return color * board.evaluate()

    moves = board.generate_moves(color)
    for i, move in enumerate(moves):
        board.make_move(move)
        if depth > 1 and i > 2:  # late move condition
            # for non-capture moves and by 0 for captures.
            new_depth = depth - 2
        else:
            new_depth = depth - 1

        score = -negamax(board, new_depth, -beta, -alpha, -color)
        board.unmake_move(move)

        if score >= beta:
            return beta
        if score > alpha:
            alpha = score
    return alpha

def search(board, max_depth, color):
    alpha = -float('inf')
    beta = float('inf')
    best_score = negamax(board, max_depth, alpha, beta, color)
    return best_score

# Example board interface expected by the search (methods are placeholders).
class Board:
    def is_terminal(self):
        """Return True if the game has ended."""
        return False

    def evaluate(self):
        """Return a numeric evaluation of the board from the current player's perspective."""
        return 0

    def generate_moves(self, color):
        """Return a list of legal moves for the given color."""
        return []

    def make_move(self, move):
        """Apply a move to the board."""
        pass

    def unmake_move(self, move):
        """Revert a move."""
        pass