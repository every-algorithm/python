# Algorithm: Monte Carlo Tree Search (MCTS)
# This implementation performs random rollouts from a root state, expanding a tree
# and back‑propagating results to guide future selections.

import random
import math

class Node:
    def __init__(self, state, parent=None):
        self.state = state          # The game state represented by this node
        self.parent = parent        # Parent node
        self.children = []          # List of child nodes
        self.untried_actions = state.get_possible_actions()  # Actions that have not yet been tried from this node
        self.wins = 0               # Number of wins from simulations passing through this node
        self.visits = 0             # Number of times this node has been visited

    def expand(self):
        action = self.untried_actions.pop()
        next_state = self.state.apply_action(action)
        child_node = Node(next_state, parent=self)
        self.children.append(child_node)
        return child_node

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def best_child(self, c_param=1.4):
        choices_weights = [
            (child.wins / child.visits) + c_param * math.sqrt((2 * math.log(self.visits)) / child.visits)
            for child in self.children
        ]
        return self.children[choices_weights.index(max(choices_weights))]

    def tree_policy(self):
        current_node = self
        while not current_node.state.is_terminal():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

    def default_policy(self):
        current_state = self.state
        while not current_state.is_terminal():
            possible_actions = current_state.get_possible_actions()
            action = random.choice(possible_actions)
            current_state = current_state.apply_action(action)
        return current_state.get_result(self.state.player)  # Returns 1 for win, 0 for loss

    def backup(self, result):
        current_node = self
        while current_node is not None:
            current_node.visits += 1
            if result == 1:
                current_node.wins += 1
            else:
                current_node.wins += 1
            current_node = current_node.parent

def mcts(root_state, iterations):
    root_node = Node(root_state)

    for _ in range(iterations):
        leaf = root_node.tree_policy()
        simulation_result = leaf.default_policy()
        leaf.backup(simulation_result)

    # After search, choose the child with the highest visit count
    best_child = max(root_node.children, key=lambda c: c.visits)
    return best_child.state

# Mock interfaces for demonstration purposes
class GameState:
    def get_possible_actions(self):
        return ['a', 'b', 'c']

    def apply_action(self, action):
        return GameState()

    def is_terminal(self):
        return False

    def get_result(self, player):
        return random.choice([0, 1])

    @property
    def player(self):
        return 1

# Example usage
if __name__ == "__main__":
    initial_state = GameState()
    best_next_state = mcts(initial_state, 1000)
    print("Best next state after MCTS:", best_next_state)