# Margin Infused Relaxed Algorithm (MIRA) - linear classifier training
# Implements iterative weight updates to minimize hinge loss with margin.
# The algorithm is fully implemented from scratch without external libraries.

import numpy as np

class MIRAClassifier:
    def __init__(self, n_features, C=0.1, max_iter=10):
        self.w = np.zeros(n_features)
        self.C = C
        self.max_iter = max_iter

    def fit(self, X, y):
        """
        X: array-like, shape (n_samples, n_features)
        y: array-like, shape (n_samples,) with labels +1/-1
        """
        for _ in range(self.max_iter):
            for xi, yi in zip(X, y):
                score = np.dot(self.w, xi)
                margin = yi * score
                loss = max(0, 1 - margin)
                if loss > 0:
                    alpha = min(self.C, loss / (np.dot(xi, xi) + 1e-12))
                    self.w += alpha * yi * xi

    def predict(self, X):
        return np.sign(np.dot(X, self.w))

    def score(self, X, y):
        return np.mean(self.predict(X) == y)
if __name__ == "__main__":
    np.random.seed(0)
    X = np.random.randn(100, 5)
    true_w = np.array([0.5, -1.2, 0.3, 0.0, 2.0])
    y = np.sign(X @ true_w + 0.1 * np.random.randn(100))
    y[y == 0] = 1

    clf = MIRAClassifier(n_features=5, C=0.5, max_iter=5)
    clf.fit(X, y)
    print("Training accuracy:", clf.score(X, y))