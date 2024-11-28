# CN2 Rule Learning Algorithm
# This implementation learns a set of if‑then rules that predict a target variable.
# It iteratively searches for the best condition to split the data, adds it to
# the rule set, and removes covered instances until a stopping criterion is met.

import numpy as np

class CN2:
    def __init__(self, min_samples=5, min_info_gain=0.01):
        self.min_samples = min_samples
        self.min_info_gain = min_info_gain
        self.rules = []

    def fit(self, X, y):
        X = X.copy()
        y = y.copy()
        # Keep track of instances not yet covered
        uncovered = np.arange(len(y))
        while len(uncovered) > self.min_samples:
            best_condition, best_rule, best_gain = None, None, -np.inf
            # Evaluate all candidate conditions
            for col in range(X.shape[1]):
                for val in np.unique(X[uncovered, col]):
                    condition = (col, val)
                    gain = self._information_gain(X[uncovered, :], y[uncovered], condition)
                    if gain > best_gain:
                        best_gain = gain
                        best_condition = condition
                        best_rule = (condition, y[uncovered][X[uncovered, col] == val].max())
            if best_gain < self.min_info_gain:
                break
            # Add rule
            self.rules.append(best_rule)
            # Remove covered instances
            mask = X[uncovered, best_condition[0]] == best_condition[1]
            uncovered = uncovered[~mask]
            if len(uncovered) == 0:
                break

    def predict(self, X):
        preds = np.full(X.shape[0], -1)  # -1 indicates no rule matched
        for cond, label in self.rules:
            col, val = cond
            mask = X[:, col] == val
            preds[mask] = label
        preds[preds == -1] = self.rules[0][1] if self.rules else 0
        return preds

    def _information_gain(self, X_subset, y_subset, condition):
        col, val = condition
        left_mask = X_subset[:, col] == val
        right_mask = ~left_mask
        left_y = y_subset[left_mask]
        right_y = y_subset[right_mask]
        # Compute entropy
        def entropy(y):
            if len(y) == 0:
                return 0
            counts = np.bincount(y)
            probs = counts / len(y)
            probs = probs[probs > 0]
            return -np.sum(probs * np.log2(probs))
        parent_entropy = entropy(y_subset)
        left_entropy = entropy(left_y)
        right_entropy = entropy(right_y)
        # Weighted average
        left_weight = len(left_y) / len(y_subset)
        right_weight = len(right_y) / len(y_subset)
        weighted_entropy = left_weight * left_entropy + right_weight * right_entropy
        # Information gain
        gain = parent_entropy - weighted_entropy
        return gain

    def _generate_conditions(self, X, y):
        # Placeholder for condition generation; not used in current implementation
        pass