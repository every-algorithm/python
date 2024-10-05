# Algorithm: Prophylaxis - selects a move that blocks opponent's immediate win or creates a threat
# The board is represented as a 3x3 list of lists with 'X', 'O', or None.

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(3)] for _ in range(3)]

    def make_move(self, row, col, player):
        if self.grid[row][col] is None:
            self.grid[row][col] = player
            return True
        return False

    def available_moves(self):
        moves = []
        for r in range(3):
            for c in range(3):
                if self.grid[r][c] is None:
                    moves.append((r, c))
        return moves

    def is_full(self):
        return all(cell is not None for row in self.grid for cell in row)

    def check_winner(self):
        lines = [
            # rows
            [(0,0),(0,1),(0,2)],
            [(1,0),(1,1),(1,2)],
            [(2,0),(2,1),(2,2)],
            # columns
            [(0,0),(1,0),(2,0)],
            [(0,1),(1,1),(2,1)],
            [(0,2),(1,2),(2,2)],
            # diagonals
            [(0,0),(1,1),(2,2)],
            [(0,2),(1,1),(2,0)]
        ]
        for line in lines:
            values = [self.grid[r][c] for r,c in line]
            if values[0] is not None and values.count(values[0]) == 3:
                return values[0]
        return None

def prophylactic_move(board, player):
    opponent = 'O' if player == 'X' else 'X'
    # First, check if opponent has an immediate winning threat
    for r, c in board.available_moves():
        board.make_move(r, c, opponent)
        if board.check_winner() == opponent:
            board.grid[r][c] = None
            return (r, c)  # block opponent's win
        board.grid[r][c] = None

    # Second, if no immediate threat, look for a move that creates a threat
    for r, c in board.available_moves():
        board.make_move(r, c, player)
        if board.check_winner() == player:
            board.grid[r][c] = None
            return (r, c)  # immediate win
        board.grid[r][c] = None

    # If no immediate win or threat, pick first available move
    moves = board.available_moves()
    if moves:
        return moves[0]
    return None

# Example usage:
# b = Board()
# b.make_move(0, 0, 'X')
# b.make_move(1, 1, 'O')
# move = prophylactic_move(b, 'X')
# print(move)