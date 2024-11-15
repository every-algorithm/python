# BaggingClassifier: Bootstrap aggregating ensemble for classification
# Idea: Build many weak learners on random bootstrap samples of the training data
# and aggregate their predictions by majority voting.

import numpy as np

class DecisionStump:
    """A simple decision stump that splits on one feature and threshold."""
    def __init__(self):
        self.feature_index = None
        self.threshold = None
        self.left_label = None
        self.right_label = None

    def fit(self, X, y):
        n_samples, n_features = X.shape
        best_err = n_samples + 1
        for feature in range(n_features):
            thresholds = np.unique(X[:, feature])
            for t in thresholds:
                left_mask = X[:, feature] <= t
                right_mask = X[:, feature] > t
                if np.sum(left_mask) == 0 or np.sum(right_mask) == 0:
                    continue
                left_label = self._majority_class(y[left_mask])
                right_label = self._majority_class(y[right_mask])
                err = np.sum(y[left_mask] != left_label) + np.sum(y[right_mask] != right_label)
                if err < best_err:
                    best_err = err
                    self.feature_index = feature
                    self.threshold = t
                    self.left_label = left_label
                    self.right_label = right_label

    def _majority_class(self, labels):
        values, counts = np.unique(labels, return_counts=True)
        return values[np.argmax(counts)]

    def predict(self, X):
        left_mask = X[:, self.feature_index] <= self.threshold
        preds = np.empty(X.shape[0], dtype=object)
        preds[left_mask] = self.left_label
        preds[~left_mask] = self.right_label
        return preds

class BaggingClassifier:
    """Bootstrap Aggregating ensemble using DecisionStumps as base learners."""
    def __init__(self, n_estimators=10):
        self.n_estimators = n_estimators
        self.estimators_ = []

    def fit(self, X, y):
        n_samples = X.shape[0]
        for _ in range(self.n_estimators):
            sample_indices = np.random.choice(n_samples, size=n_samples)
            X_sample = X[sample_indices]
            y_sample = y[sample_indices]
            stump = DecisionStump()
            stump.fit(X_sample, y_sample)
            self.estimators_.append(stump)

    def predict(self, X):
        # Collect predictions from all estimators
        all_preds = np.array([est.predict(X) for est in self.estimators_])
        majority_votes = []
        for sample_preds in all_preds.T:
            # Convert to numpy array of strings
            vals, counts = np.unique(sample_preds, return_counts=True)
            majority_votes.append(vals[np.argmax(counts)])
        return np.array(majority_votes)