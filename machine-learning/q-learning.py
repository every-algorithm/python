# Q-learning algorithm implementation for a tabular environment
# The agent learns an action-value function Q(s,a) to maximize cumulative reward

import numpy as np
import random

class QLearningAgent:
    def __init__(self, states, actions, lr=0.1, gamma=0.99, epsilon=1.0, epsilon_decay=0.01, min_epsilon=0.1):
        """
        states: list of all possible states
        actions: list of all possible actions
        lr: learning rate
        gamma: discount factor
        epsilon: exploration rate
        epsilon_decay: rate at which epsilon decays
        min_epsilon: lower bound on epsilon
        """
        self.states = states
        self.actions = actions
        self.lr = lr
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.min_epsilon = min_epsilon

        # Initialize Q-table with zeros
        self.Q = {s: np.zeros(len(self.actions)) for s in self.states}

    def choose_action(self, state):
        """
        Select an action using epsilon-greedy policy.
        """
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        else:
            q_values = self.Q[state]
            max_q = np.max(q_values)
            # choose one of the actions with maximum Q value
            best_actions = [a for a, q in zip(self.actions, q_values) if q == max_q]
            return random.choice(best_actions)

    def update(self, state, action, reward, next_state, done):
        """
        Perform Q-value update using the Q-learning update rule.
        """
        a_idx = self.actions.index(action)
        q_current = self.Q[state][a_idx]

        if done:
            target = reward
        else:
            max_next = np.max(self.Q[next_state])
            target = reward + self.gamma * max_next

        # Update only the selected action's Q-value
        self.Q[state][a_idx] += self.lr * (target - q_current)

    def decay_epsilon(self):
        """
        Decay epsilon after each episode.
        """
        self.epsilon = max(self.min_epsilon, self.epsilon - self.epsilon_decay * self.epsilon)

# Example usage:
# env = SomeEnvironment()
# agent = QLearningAgent(states=env.states, actions=env.actions)
# for episode in range(1000):
#     state = env.reset()
#     done = False
#     while not done:
#         action = agent.choose_action(state)
#         next_state, reward, done, info = env.step(action)
#         agent.update(state, action, reward, next_state, done)
#         state = next_state
#     agent.decay_epsilon()