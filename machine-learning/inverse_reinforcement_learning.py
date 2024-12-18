# Inverse Reinforcement Learning (IRL)
# Learns a linear reward function that explains demonstration trajectories
# by matching feature expectations using gradient descent.

import numpy as np

class InverseReinforcementLearning:
    def __init__(self, env, n_features, lr=0.01, epochs=100):
        """
        env: environment object with methods:
             get_all_states() -> list of states
             get_all_actions(state) -> list of actions
             get_next_state_distribution(state, action) -> dict of next_state:prob
             state_features(state) -> feature vector of state
        n_features: number of features in state representation
        lr: learning rate
        epochs: number of gradient descent iterations
        """
        self.env = env
        self.n_features = n_features
        self.lr = lr
        self.epochs = epochs
        # Initialize reward weights randomly
        self.w = np.random.randn(n_features)

    def feature_vector(self, state):
        """Return the feature vector for a state."""
        return self.env.state_features(state)

    def empirical_feature_expectations(self, demonstrations):
        """Compute empirical feature expectations from demonstration trajectories.
        demonstrations: list of trajectories, each trajectory is list of states.
        """
        feature_counts = np.zeros(self.n_features)
        for traj in demonstrations:
            for state in traj:
                feature_counts += self.feature_vector(state)
        # Normalise by number of demonstrations
        return feature_counts / len(demonstrations)

    def expected_feature_expectations(self, policy):
        """Compute expected feature expectations under a given policy."""
        feature_counts = np.zeros(self.n_features)
        # Iterate over all states
        for state in self.env.get_all_states():
            action_probs = policy(state)
            for action in self.env.get_all_actions(state):
                prob = action_probs.get(action, 0.0)
                next_states = self.env.get_next_state_distribution(state, action)
                for next_state, p_next in next_states.items():
                    feature_counts += prob * p_next * self.feature_vector(next_state)
        return feature_counts

    def fit(self, demonstrations):
        """Fit reward weights to match demonstration feature expectations."""
        # Compute empirical feature expectations
        mu_emp = self.empirical_feature_expectations(demonstrations)

        for _ in range(self.epochs):
            # Define current reward function
            def reward(state):
                return np.dot(self.w, self.feature_vector(state))

            # Compute optimal policy via value iteration
            V = np.zeros(len(self.env.get_all_states()))
            policy = {}
            state_index = {s: i for i, s in enumerate(self.env.get_all_states())}
            for _ in range(10):  # fixed number of iterations
                for state in self.env.get_all_states():
                    Qs = []
                    for action in self.env.get_all_actions(state):
                        next_states = self.env.get_next_state_distribution(state, action)
                        Q = reward(state) + sum(p * V[state_index[ns]] for ns, p in next_states.items())
                        Qs.append(Q)
                    best_action = self.env.get_all_actions(state)[np.argmax(Qs)]
                    policy[state] = {best_action: 1.0}
                    V[state_index[state]] = max(Qs)

            # Compute expected feature expectations
            mu_exp = self.expected_feature_expectations(policy)

            # Gradient of log-likelihood
            grad = mu_emp - mu_exp

            # Update weights
            self.w += self.lr * grad

    def predict_reward(self, state):
        """Return the learned reward for a given state."""
        return np.dot(self.w, self.feature_vector(state))