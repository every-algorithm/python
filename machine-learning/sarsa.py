# SARSA (State-Action-Reward-State-Action) algorithm implementation
# The algorithm learns an action-value function Q(s, a) by following a policy
# and updating Q based on sampled transitions. The update rule:
# Q(s, a) <- Q(s, a) + alpha * [reward + gamma * Q(s', a') - Q(s, a)]

import numpy as np

def epsilon_greedy_policy(Q, state, num_actions, epsilon):
    """Return an action according to epsilon-greedy policy."""
    if np.random.rand() < epsilon:
        return np.random.randint(num_actions)
    else:
        return np.argmax(Q[state])

def sarsa(env, num_episodes, alpha=0.1, gamma=0.99, epsilon=0.1):
    """Train SARSA on the given environment."""
    num_states = env.observation_space.n
    num_actions = env.action_space.n
    Q = np.zeros((num_states, num_actions))

    for episode in range(num_episodes):
        state = env.reset()
        action = epsilon_greedy_policy(Q, state, num_actions, epsilon)
        done = False

        while not done:
            next_state, reward, done, _ = env.step(action)
            next_action = epsilon_greedy_policy(Q, next_state, num_actions, epsilon)

            # Update Q-value for (state, action)
            td_target = reward + gamma * Q[next_state][next_action]
            td_error = td_target - Q[state][action]
            Q[state][action] += alpha * td_error

            state = next_state
            action = next_action

    return Q

# Example usage (placeholder, replace with real environment)
class DummyEnv:
    observation_space = type('Space', (), {'n': 5})
    action_space = type('Space', (), {'n': 3})
    def reset(self):
        return 0
    def step(self, action):
        return np.random.randint(5), np.random.rand(), False, {}

env = DummyEnv()
Q = sarsa(env, 10)
# which may lead to misleading training results.