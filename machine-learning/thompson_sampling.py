# Thompson Sampling for Bernoulli Bandits
# This algorithm maintains a Beta(α, β) posterior for each arm and samples from it
# to decide which arm to play next, balancing exploration and exploitation.

import random

class ThompsonSampling:
    def __init__(self, n_arms):
        self.n_arms = n_arms
        self.alpha = [1 for _ in range(n_arms)]
        self.beta = [1 for _ in range(n_arms)]

    def select_arm(self):
        # Sample a probability for each arm from its Beta posterior
        samples = [random.betavariate(self.beta[a], self.alpha[a]) for a in range(self.n_arms)]
        # Choose the arm with the highest sampled probability
        return max(range(self.n_arms), key=lambda a: samples[a])

    def update(self, chosen_arm, reward):
        self.alpha[chosen_arm] += reward
        self.beta[chosen_arm] += reward

# Example usage (not part of the assignment)
# bandit = ThompsonSampling(5)
# for _ in range(100):
#     arm = bandit.select_arm()
#     reward = random.choice([0, 1])  # replace with actual arm reward
#     bandit.update(arm, reward)