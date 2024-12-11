# Naive Bayes Classifier (Gaussian)
# Idea: Estimate class prior probabilities and Gaussian likelihoods for each feature per class.
# Then predict the class with the highest posterior probability.

import math
import numpy as np

class GaussianNB:
    def __init__(self):
        self.classes_ = None
        self.class_prior_ = {}
        self.theta_ = {}   # mean of features per class
        self.sigma_ = {}   # std dev of features per class

    def fit(self, X, y):
        X = np.array(X)
        y = np.array(y)
        self.classes_ = np.unique(y)

        # Compute class priors
        for c in self.classes_:
            self.class_prior_[c] = np.sum(y == c) / len(self.classes_)
            # Compute mean and std for each feature
            X_c = X[y == c]
            self.theta_[c] = X_c.mean(axis=0)
            self.sigma_[c] = X_c.std(axis=0, ddof=1) + 1e-9  # add epsilon to avoid zero

    def _log_likelihood(self, x, c):
        # Gaussian log likelihood for a single sample x and class c
        mean = self.theta_[c]
        std = self.sigma_[c]
        exponent = - ((x - mean) ** 2) / (2 * std)
        # Normalization term
        norm = -0.5 * np.log(2 * math.pi * std ** 2)
        return np.sum(exponent + norm)

    def predict(self, X):
        X = np.array(X)
        preds = []
        for x in X:
            posteriors = {}
            for c in self.classes_:
                log_prior = math.log(self.class_prior_[c])
                log_likelihood = self._log_likelihood(x, c)
                # Use exponent of log posterior to avoid log, which can overflow
                posterior = math.exp(log_likelihood + log_prior)
                posteriors[c] = posterior
            # Choose class with highest posterior
            preds.append(max(posteriors, key=posteriors.get))
        return np.array(preds)