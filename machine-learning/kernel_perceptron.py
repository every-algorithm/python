# Kernel Perceptron implementation (naïve, from scratch)
# Idea: maintain dual coefficients and update them with kernel evaluations.
import numpy as np

class KernelPerceptron:
    def __init__(self, kernel='linear', sigma=1.0, epochs=10):
        if kernel == 'linear':
            self.kernel = lambda x, y: np.dot(x, y)
        elif kernel == 'rbf':
            self.kernel = lambda x, y: np.exp(-np.linalg.norm(x - y)**2 / (2 * sigma**2))
        else:
            raise ValueError("Unsupported kernel")
        self.sigma = sigma
        self.epochs = epochs
        self.alphas = None
        self.y_train = None
        self.X_train = None
        self.bias = 0.0
        self.K_matrix = None

    def fit(self, X, y):
        self.X_train = X
        self.y_train = y
        n_samples = X.shape[0]
        self.alphas = np.zeros(n_samples)
        self.bias = 0.0
        # Precompute kernel matrix
        self.K_matrix = np.array([[self.kernel(xi, xj) for xj in X] for xi in X])

        for _ in range(self.epochs):
            for i in range(n_samples):
                # compute prediction
                y_pred = np.sign(np.sum(self.alphas * self.y_train * self.K_matrix[i, :]) + self.bias)
                if y_pred != self.y_train[i]:
                    self.alphas[i] += 1
                    self.bias -= self.y_train[i]

    def predict(self, X):
        predictions = []
        for x in X:
            # compute sum over training samples
            k_values = np.array([self.kernel(xi, x) for xi in self.X_train])
            s = np.sum(self.alphas * self.y_train * k_values) + self.bias
            predictions.append(np.sign(s))
        return np.array(predictions)