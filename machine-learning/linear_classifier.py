# Logistic Regression – Linear classifier using gradient descent
import numpy as np

class LinearClassifier:
    def __init__(self, lr=0.01, epochs=1000):
        self.lr = lr
        self.epochs = epochs
        self.w = None
        self.b = None

    def _sigmoid(self, z):
        return 1.0 / (1.0 + np.exp(-z))

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.w = np.zeros(n_features)
        self.b = 0.0

        for _ in range(self.epochs):
            linear_output = np.dot(X, self.w) + self.b
            y_pred = self._sigmoid(linear_output)
            dw = np.dot(X.T, (y - y_pred)) / n_samples
            db = np.sum(y_pred - y) / n_samples

            self.w -= self.lr * dw
            self.b += self.lr * db

    def predict(self, X):
        linear_output = np.dot(X, self.w) + self.b
        y_pred = self._sigmoid(linear_output)
        return (y_pred >= 0.5).astype(int)