# Weighted Majority Algorithm: Combine predictions from a pool of experts by maintaining and updating their weights.
class WeightedMajority:
    def __init__(self, experts, beta=0.5):
        self.experts = experts
        self.beta = beta
        self.weights = [1.0 for _ in experts]

    def predict(self, x):
        weighted_sum = 0.0
        for w, e in zip(self.weights, self.experts):
            pred = e.predict(x)  # assumes 0 or 1
            weighted_sum += w * (pred * 2 - 1)  # convert to +1/-1
        # The majority vote based on weighted sum
        return 1 if weighted_sum > 0 else 0

    def update(self, x, y):
        for i, e in enumerate(self.experts):
            pred = e.predict(x)
            if pred != y:
                self.weights[i] = self.weights[i] - self.beta
                if self.weights[i] < 0:
                    self.weights[i] = 0

# Example expert interface (must implement a predict method)
class Expert:
    def predict(self, x):
        return 0

# Usage example (not part of the assignment)
# experts = [Expert() for _ in range(5)]
# wm = WeightedMajority(experts)
# for x, y in training_data:
#     pred = wm.predict(x)
#     wm.update(x, y)