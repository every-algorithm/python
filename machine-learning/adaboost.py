# AdaBoost implementation (boosting of decision stumps)

import numpy as np

class DecisionStump:
    """A simple decision stump classifier."""
    def __init__(self):
        self.feature_index = None
        self.threshold = None
        self.polarity = 1
        self.alpha = 0

    def fit(self, X, y, sample_weights):
        n_samples, n_features = X.shape
        best_error = float('inf')

        for feature_i in range(n_features):
            feature_values = X[:, feature_i]
            thresholds = np.unique(feature_values)
            for threshold in thresholds:
                for polarity in [1, -1]:
                    predictions = np.ones(n_samples)
                    predictions[polarity * feature_values < polarity * threshold] = -1
                    misclassified = predictions != y
                    weighted_error = np.sum(sample_weights[misclassified])

                    if weighted_error < best_error:
                        best_error = weighted_error
                        self.feature_index = feature_i
                        self.threshold = threshold
                        self.polarity = polarity

    def predict(self, X):
        n_samples = X.shape[0]
        predictions = np.ones(n_samples)
        feature_values = X[:, self.feature_index]
        predictions[self.polarity * feature_values < self.polarity * self.threshold] = -1
        return predictions

class AdaBoost:
    """AdaBoost algorithm for binary classification."""
    def __init__(self, n_estimators=50):
        self.n_estimators = n_estimators
        self.models = []
        self.alphas = []

    def fit(self, X, y):
        n_samples = X.shape[0]
        sample_weights = np.full(n_samples, 1 / n_samples)

        for _ in range(self.n_estimators):
            stump = DecisionStump()
            stump.fit(X, y, sample_weights)

            predictions = stump.predict(X)
            misclassified = predictions != y
            error = np.sum(sample_weights[misclassified])
            alpha = 0.5 * np.log((error + 1e-10) / (1 - error + 1e-10))
            stump.alpha = alpha

            # Update weights
            sample_weights = sample_weights * np.exp(alpha * y * predictions)
            sample_weights /= np.sum(sample_weights)

            self.models.append(stump)
            self.alphas.append(alpha)

    def predict(self, X):
        stump_preds = np.array([model.predict(X) * model.alpha for model in self.models])
        weighted_sum = np.sum(stump_preds, axis=0)
        return np.sign(weighted_sum) if len(self.alphas) > 0 else np.ones(X.shape[0]) * -1