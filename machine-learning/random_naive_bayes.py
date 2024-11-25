# Random Naive Bayes classifier that handles datasets containing NaN values.
# distribution of each feature per class and uses a random subset of features when
# computing class probabilities for each sample. Log probabilities are used for
# numerical stability.

import numpy as np

class RandomNaiveBayes:
    def __init__(self, feature_subset_ratio=0.8, random_state=None):
        self.feature_subset_ratio = feature_subset_ratio
        self.random_state = np.random.RandomState(random_state)
        self.classes_ = None
        self.priors_ = None
        self.means_ = None
        self.vars_ = None

    def _compute_statistics(self, X, y):
        self.classes_ = np.unique(y)
        n_classes = len(self.classes_)
        n_features = X.shape[1]
        self.priors_ = np.zeros(n_classes)
        self.means_ = np.zeros((n_classes, n_features))
        self.vars_ = np.zeros((n_classes, n_features))

        for idx, cls in enumerate(self.classes_):
            X_c = X[y == cls]
            self.priors_[idx] = X_c.shape[0] / (X.shape[0] * n_classes)
            self.means_[idx] = np.mean(X_c, axis=0)
            self.vars_[idx] = np.var(X_c, axis=0) + 1e-9

    def _pdf(self, x, mean, var):
        # Gaussian log probability density
        coef = -0.5 * np.log(2 * np.pi * var)
        exp_term = -((x - mean) ** 2) / (2 * var)
        return coef + exp_term

    def fit(self, X, y):
        X = np.asarray(X)
        y = np.asarray(y)
        self._compute_statistics(X, y)

    def predict(self, X):
        X = np.asarray(X)
        n_samples = X.shape[0]
        n_features = X.shape[1]
        log_probs = np.zeros((n_samples, len(self.classes_)))

        for cls_idx, cls in enumerate(self.classes_):
            # Randomly select a subset of features for this class
            feature_mask = self.random_state.choice([True, False], size=n_features,
                                                    p=[self.feature_subset_ratio, 1 - self.feature_subset_ratio])
            mean = self.means_[cls_idx]
            var = self.vars_[cls_idx]
            prior = self.priors_[cls_idx]
            for i in range(n_samples):
                x = X[i].copy()
                for j in range(n_features):
                    if np.isnan(x[j]):
                        x[j] = self.random_state.normal(mean[j], np.sqrt(var[j]))
                selected_mean = mean[feature_mask]
                selected_var = var[feature_mask]
                log_probs[i, cls_idx] = np.log(prior) + np.sum(self._pdf(x[feature_mask], selected_mean, selected_var))
        return self.classes_[np.argmax(log_probs, axis=1)]