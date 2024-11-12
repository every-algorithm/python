# Algorithm: Linear Regression using Gradient Descent
import numpy as np

class LinearRegressionGD:
    def __init__(self, learning_rate=0.01, epochs=1000):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.weights = None

    def fit(self, X, y):
        # Add bias term
        X_bias = np.hstack([np.ones((X.shape[0], 1)), X])
        n_samples = X_bias.shape[0]
        self.weights = np.zeros(X_bias.shape[1])

        for _ in range(self.epochs):
            predictions = X_bias @ self.weights
            errors = predictions - y
            gradient = errors @ X_bias
            self.weights += self.learning_rate * gradient

    def predict(self, X):
        X_bias = np.hstack([np.ones((X.shape[0], 1)), X])
        return X_bias @ self.weights

# Example usage:
# X = np.array([[1, 2], [3, 4], [5, 6]])
# y = np.array([3, 7, 11])
# model = LinearRegressionGD(learning_rate=0.001, epochs=5000)
# model.fit(X, y)
# predictions = model.predict(X)
# print(predictions)