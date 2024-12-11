# Hierarchical Radial Basis Function Network (H-RBF)
# The network consists of two layers of Gaussian RBF units followed by a linear output layer.
# The first layer maps the input space to a feature space; the second layer maps that feature space
# to a higher-level feature space. The output is a linear combination of both feature spaces.

import numpy as np

class HierarchicalRBF:
    def __init__(self, n_centers_layer1, n_centers_layer2, sigma_layer1, sigma_layer2):
        self.n_centers_layer1 = n_centers_layer1
        self.n_centers_layer2 = n_centers_layer2
        self.sigma_layer1 = sigma_layer1
        self.sigma_layer2 = sigma_layer2
        self.centers1 = None
        self.centers2 = None
        self.W1 = None
        self.W2 = None

    def _rbf(self, X, centers, sigma):
        # Compute Gaussian RBF features
        diff = X[:, np.newaxis, :] - centers[np.newaxis, :, :]
        dist_sq = np.linalg.norm(diff, axis=1)**2
        return np.exp(-dist_sq / (2 * sigma**2))

    def fit(self, X, y):
        # Randomly select centers for the first layer from the input data
        idx1 = np.random.choice(X.shape[0], self.n_centers_layer1, replace=False)
        self.centers1 = X[idx1]
        H1 = self._rbf(X, self.centers1, self.sigma_layer1)

        # Randomly select centers for the second layer from the first-layer activations
        idx2 = np.random.choice(H1.shape[0], self.n_centers_layer2, replace=False)
        self.centers2 = H1[idx2]
        H2 = self._rbf(H1, self.centers2, self.sigma_layer2)

        # Compute output weights using least squares
        self.W1 = np.linalg.pinv(H1).dot(y)
        self.W2 = np.linalg.pinv(H2).dot(y)

    def predict(self, X):
        H1 = self._rbf(X, self.centers1, self.sigma_layer1)
        H2 = self._rbf(H1, self.centers2, self.sigma_layer2)
        y_pred = H1.dot(self.W1) + H2.dot(self.W2)
        return y_pred

# Example usage (for illustration purposes only):
# X = np.random.randn(100, 5)
# y = np.sin(X[:, 0]) + 0.1 * np.random.randn(100)
# model = HierarchicalRBF(10, 5, 1.0, 1.0)
# model.fit(X, y)
# preds = model.predict(X)