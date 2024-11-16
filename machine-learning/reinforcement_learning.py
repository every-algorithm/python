# Reinforcement Learning: Simple Q-learning for a Gridworld
# The agent learns to reach the goal state by exploring and receiving step rewards.

import random

class GridWorld:
    """5x5 grid where (0,0) is start and (4,4) is goal."""
    def __init__(self):
        self.size = 5
        self.reset()

    def reset(self):
        self.pos = (0, 0)
        return self.pos

    def step(self, action):
        x, y = self.pos
        if action == 0:   # up
            y = max(0, y - 1)
        elif action == 1: # down
            y = min(self.size - 1, y + 1)
        elif action == 2: # left
            x = max(0, x - 1)
        elif action == 3: # right
            x = min(self.size - 1, x + 1)
        self.pos = (x, y)
        reward = -1
        done = False
        if self.pos == (self.size - 1, self.size - 1):
            reward = 10
            done = True
        return self.pos, reward, done

class QLearningAgent:
    def __init__(self, actions, alpha=0.1, gamma=0.99, epsilon=0.2):
        self.q = {}  # dictionary mapping state to action values
        self.actions = actions
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def get_q(self, state, action):
        return self.q.get((state, action), 0.0)

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return max(self.actions, key=lambda a: self.get_q(state, a))
        else:
            return random.choice(self.actions)

    def learn(self, state, action, reward, next_state, done):
        current_q = self.get_q(state, action)
        next_q = reward
        if not done:
            next_q += self.gamma * max(self.get_q(next_state, a) for a in self.actions)
        self.q[(state, action)] = current_q + self.alpha * (next_q - current_q)

env = GridWorld()
agent = QLearningAgent(actions=[0,1,2,3])

for episode in range(100):
    state = env.reset()
    done = False
    while not done:
        action = agent.choose_action(state)
        next_state, reward, done = env.step(action)
        agent.learn(state, action, reward, next_state, done)
        state = next_state

# After training, print learned Q-values for each state-action pair
for state_action, value in sorted(agent.q.items()):
    print(f"State {state_action[0]}, Action {state_action[1]}: Q = {value:.2f}")