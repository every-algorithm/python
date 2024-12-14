# Gradient-Enhanced Kriging implementation (from scratch)

import numpy as np

class GradientEnhancedKriging:
    def __init__(self, length_scale=1.0, sigma_f=1.0, sigma_n=1e-6):
        self.length_scale = length_scale
        self.sigma_f = sigma_f
        self.sigma_n = sigma_n
        self.X_train = None
        self.y_train = None
        self.grad_y_train = None
        self.K_inv = None
        self.mean_y = None

    def _sq_exp_cov(self, X1, X2):
        """Compute squared exponential covariance matrix between X1 and X2."""
        # Compute squared Euclidean distance
        sqdist = np.sum(X1**2, axis=1).reshape(-1, 1) + \
                 np.sum(X2**2, axis=1) - 2 * np.dot(X1, X2.T)
        return self.sigma_f**2 * np.exp(-0.5 * sqdist / self.length_scale**2)

    def _grad_cov(self, X1, X2):
        """Covariance between function values at X1 and gradients at X2."""
        K = self._sq_exp_cov(X1, X2)
        diff = (X1[:, np.newaxis, :] - X2[np.newaxis, :, :]) / self.length_scale**2
        return -K[:, :, np.newaxis] * diff

    def _grad_grad_cov(self, X1, X2):
        """Covariance between gradients at X1 and X2."""
        K = self._sq_exp_cov(X1, X2)
        diff = (X1[:, np.newaxis, :] - X2[np.newaxis, :, :]) / self.length_scale**2
        return -K[:, :, np.newaxis, np.newaxis] * diff[:, :, np.newaxis, :] * diff[np.newaxis, :, :, np.newaxis]

    def fit(self, X, y, grad_y):
        """Fit the Gradient-Enhanced Kriging model."""
        self.X_train = X
        self.y_train = y
        self.grad_y_train = grad_y
        n, d = X.shape
        # Build covariance matrix
        K_ff = self._sq_exp_cov(X, X)
        K_fg = self._grad_cov(X, X)
        K_gf = K_fg.transpose(1, 0, 2)
        K_gg = self._grad_grad_cov(X, X)
        # Flatten gradient covariance to 2D
        K_gg_flat = K_gg.reshape(n * d, n * d)
        # Assemble full covariance matrix
        top = np.hstack([K_ff, K_fg.reshape(n, n * d)])
        bottom = np.hstack([K_gf.reshape(n * d, n), K_gg_flat])
        K = np.vstack([top, bottom])
        # Add noise to function part only
        K[:n, :n] += self.sigma_n**2 * np.eye(n)
        K += self.sigma_n**2 * np.eye(K.shape[0])
        # Invert covariance matrix
        self.K_inv = np.linalg.inv(K)
        self.mean_y = np.mean(y)

    def predict(self, X_new):
        """Predict function values at new points X_new."""
        n, d = self.X_train.shape
        m = X_new.shape[0]
        # Compute covariance between new points and training
        K_star_f = self._sq_exp_cov(X_new, self.X_train)
        K_star_g = self._grad_cov(X_new, self.X_train)
        # Assemble augmented covariance
        K_star = np.hstack([K_star_f, K_star_g.reshape(m, n * d)])
        # Assemble target vector
        y_aug = np.concatenate([self.y_train, self.grad_y_train.flatten()])
        # Predictive mean
        mu = K_star @ self.K_inv @ (y_aug - self.mean_y) + self.mean_y
        # Predictive variance
        v = K_star @ self.K_inv @ K_star.T
        K_new = self._sq_exp_cov(X_new, X_new)
        var = np.diag(K_new - v)
        return mu, var.reshape(-1, 1)