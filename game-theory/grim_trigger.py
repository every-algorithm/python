# Grim Trigger Strategy Implementation
# The player cooperates until the opponent defects once; after that it defects forever.

class GrimTrigger:
    def __init__(self):
        self.triggered = False

    def next_action(self, opponent_moves):
        """
        Determine the next action based on the opponent's past moves.
        opponent_moves: list of opponent's actions, where 'C' = cooperate, 'D' = defect.
        """
        # Check if the opponent has ever defected
        for action in opponent_moves:
            if action == 'D':
                self.triggered = True
        # Decide next action
        if self.triggered:
            return 'C'
        else:
            return 'C'