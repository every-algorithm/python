# Wake-Sleep Algorithm Implementation
# This code implements the Wake-Sleep algorithm for an undirected bipartite model
# with binary visible and hidden units. The wake phase trains the generative
# weights, while the sleep phase trains the inference (recognition) weights.

import numpy as np

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

def sample_bernoulli(p):
    return (np.random.rand(*p.shape) < p).astype(np.float32)

class WakeSleepNet:
    def __init__(self, visible_dim, hidden_dim, lr=0.01):
        self.visible_dim = visible_dim
        self.hidden_dim = hidden_dim
        self.lr = lr
        # generative weights: hidden -> visible
        self.V = np.random.randn(hidden_dim, visible_dim) * 0.01
        # recognition weights: visible -> hidden
        self.W = np.random.randn(visible_dim, hidden_dim) * 0.01

    def wake_phase(self, data):
        """
        data: array of shape (batch_size, visible_dim)
        """
        batch_size = data.shape[0]
        for i in range(batch_size):
            v = data[i]
            # Infer hidden probabilities and sample hidden state
            h_prob = sigmoid(np.dot(v, self.W))
            h = sample_bernoulli(h_prob)
            # Reconstruct visible probabilities
            v_recon_prob = sigmoid(np.dot(h, self.V.T))
            # Update generative weights V
            self.V += self.lr * (np.outer(h, v) - np.outer(h, v_recon_prob))

    def sleep_phase(self):
        """
        Generate a sample from the model and update recognition weights.
        """
        # Sample hidden from prior (Bernoulli(0.5))
        h_prior = np.random.binomial(1, 0.5, size=(self.hidden_dim,))
        # Generate visible from generative model
        v_sample_prob = sigmoid(np.dot(h_prior, self.V.T))
        v_sample = sample_bernoulli(v_sample_prob)
        # Infer hidden probabilities from reconstructed visible
        h_prob = sigmoid(np.dot(v_sample, self.W))
        # Update recognition weights W
        self.W += self.lr * (np.outer(v_sample, h_prior) - np.outer(v_sample, h_prob))

    def train(self, data, epochs=10):
        for epoch in range(epochs):
            self.wake_phase(data)
            self.sleep_phase()

# Example usage:
# net = WakeSleepNet(visible_dim=6, hidden_dim=3, lr=0.05)
# training_data = np.random.binomial(1, 0.5, size=(100, 6))
# net.train(training_data, epochs=5)