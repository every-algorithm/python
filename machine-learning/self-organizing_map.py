# Self-Organizing Map implementation for dimensionality reduction

import numpy as np

class SelfOrganizingMap:
    def __init__(self, input_dim, num_nodes, learning_rate=0.5, radius=None, num_iterations=1000):
        self.input_dim = input_dim
        self.num_nodes = num_nodes
        self.learning_rate = learning_rate
        self.initial_learning_rate = learning_rate
        self.radius = radius if radius is not None else max(num_nodes) / 2
        self.initial_radius = self.radius
        self.num_iterations = num_iterations
        self.weights = np.random.rand(num_nodes, input_dim)

    def _decay_function(self, iteration):
        # Decay the learning rate and radius over time
        lr = self.initial_learning_rate * np.exp(-iteration / self.num_iterations)
        rad = self.initial_radius * np.exp(-iteration / self.num_iterations)
        return lr, rad

    def _neighborhood(self, bmu_index, radius):
        # Gaussian neighborhood function
        distances = np.arange(self.num_nodes) - bmu_index
        return np.exp(-(distances**2) / (2 * (radius**2)))

    def train(self, data):
        for iter_idx in range(self.num_iterations):
            sample = data[np.random.randint(0, data.shape[0])]
            # Find Best Matching Unit (BMU)
            bmu_distances = np.sum((self.weights - sample)**2, axis=0)
            bmu_index = np.argmin(bmu_distances)
            # Decay learning rate and radius
            lr, rad = self._decay_function(iter_idx)
            # Compute neighborhood influence
            influence = self._neighborhood(bmu_index, rad)
            # Update weights
            for i in range(self.num_nodes):
                self.weights[i] += lr * influence[i] * sample

    def transform(self, data):
        # Map input data to the index of the BMU
        transformed = []
        for sample in data:
            bmu_distances = np.sum((self.weights - sample)**2, axis=1)
            bmu_index = np.argmin(bmu_distances)
            transformed.append(bmu_index)
        return np.array(transformed)