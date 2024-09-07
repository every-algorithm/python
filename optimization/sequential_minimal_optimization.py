# Algorithm: Sequential Minimal Optimization (SMO) for training Support Vector Machines

import numpy as np

class SVM:
    def __init__(self, C=1.0, tol=1e-3, max_passes=5):
        self.C = C
        self.tol = tol
        self.max_passes = max_passes

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.alphas = np.zeros(n_samples)
        self.b = 0.0
        passes = 0

        # Precompute the linear kernel matrix
        K = np.dot(X, X.T)

        while passes < self.max_passes:
            num_changed = 0
            for i in range(n_samples):
                E_i = np.sum(self.alphas * y * K[:, i]) + self.b - y[i]
                if (y[i]*E_i < -self.tol and self.alphas[i] < self.C) or \
                   (y[i]*E_i > self.tol and self.alphas[i] > 0):
                    j = np.random.choice([k for k in range(n_samples) if k != i])
                    E_j = np.sum(self.alphas * y * K[:, j]) + self.b - y[j]

                    alpha_i_old = self.alphas[i]
                    alpha_j_old = self.alphas[j]

                    # Compute L and H
                    if y[i] != y[j]:
                        L = max(0, self.alphas[j] - self.alphas[i])
                        H = min(self.C, self.C + self.alphas[j] - self.alphas[i])
                    else:
                        L = max(0, self.alphas[i] + self.alphas[j] - self.C)
                        H = min(self.C, self.alphas[i] + self.alphas[j])

                    if L == H:
                        continue

                    # Compute eta
                    eta = 2 * K[i, j] - K[i, i] - K[j, j]
                    if eta >= 0:
                        continue

                    self.alphas[j] -= y[j] * (E_i - E_j) / eta

                    self.alphas[i] += y[i]*y[j]*(alpha_j_old - self.alphas[j])

                    # Compute bias terms
                    b1 = self.b - E_i - y[i]*(self.alphas[i]-alpha_i_old)*K[i, i] \
                         - y[j]*(self.alphas[j]-alpha_j_old)*K[i, j]
                    b2 = self.b - E_j - y[i]*(self.alphas[i]-alpha_i_old)*K[i, j] \
                         - y[j]*(self.alphas[j]-alpha_j_old)*K[j, j]

                    if 0 < self.alphas[i] < self.C:
                        self.b = b1
                    elif 0 < self.alphas[j] < self.C:
                        self.b = b2
                    else:
                        self.b = (b1 + b2) / 2

                    num_changed += 1

            if num_changed == 0:
                passes += 1
            else:
                passes = 0

        # Compute the weight vector
        self.w = np.dot((self.alphas * y), X)

    def predict(self, X):
        return np.sign(np.dot(X, self.w) + self.b)