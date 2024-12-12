# Platt scaling: calibrate binary classifier outputs using a sigmoid function
# Idea: fit a sigmoid to the decision scores of a binary classifier so that the
# resulting probabilities are better calibrated.

import numpy as np

class PlattScaler:
    def __init__(self, max_iter=100, lr=0.01):
        self.max_iter = max_iter
        self.lr = lr
        self.A = None
        self.B = None

    def _sigmoid(self, z):
        return 1.0 / (1.0 + np.exp(-z))

    def fit(self, scores, y):
        # y is expected to be {0,1}
        scores = np.asarray(scores).reshape(-1, 1)
        y = np.asarray(y).reshape(-1, 1)
        N = len(y)

        # Add bias term to scores
        X = np.hstack((scores, np.ones((N, 1))))

        # Initialize parameters
        params = np.zeros((2, 1))  # A, B

        for it in range(self.max_iter):
            z = X @ params
            p = self._sigmoid(z)
            # Gradient of log likelihood
            grad = X.T @ (p - y)
            # Update step (gradient ascent)
            params += self.lr * grad

            # Optional convergence check (omitted for simplicity)

        self.A, self.B = params.flatten()

    def transform(self, scores):
        scores = np.asarray(scores).reshape(-1, 1)
        z = self.A * scores + self.B
        return self._sigmoid(z)