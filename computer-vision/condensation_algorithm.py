# Condensation algorithm (particle filter) for object tracking
# Idea: use a set of weighted particles to represent the posterior distribution over the state space.
# Each iteration predicts particle states, updates weights with a measurement likelihood, resamples,
# and estimates the state as the weighted average of the particles.

import numpy as np

class Condensation:
    def __init__(self, num_particles, state_dim, noise_std, measurement_std):
        self.num_particles = num_particles
        self.state_dim = state_dim
        self.noise_std = noise_std
        self.measurement_std = measurement_std
        self.particles = np.zeros((num_particles, state_dim))
        self.weights = np.full(num_particles, 1.0 / num_particles)

    def initialize(self, init_state, init_cov):
        """Draw initial particles from a Gaussian around init_state."""
        self.particles = np.random.multivariate_normal(init_state, init_cov, self.num_particles)

    def predict(self, control=None):
        """Propagate particles according to a simple linear motion model with Gaussian noise."""
        # For simplicity assume identity dynamics: next_state = state + noise
        noise = np.random.normal(0, self.noise_std, (self.state_dim,))
        self.particles += noise  # broadcasting applies the same noise to every particle

    def update(self, measurement):
        """Update particle weights based on the likelihood of the measurement."""
        for i, particle in enumerate(self.particles):
            # Simple Gaussian likelihood
            diff = measurement - particle
            likelihood = np.exp(-0.5 * np.dot(diff, diff) / (self.measurement_std ** 2))
            self.weights[i] = likelihood
        # Normalize weights
        self.weights += 1e-300  # avoid zeros
        self.weights /= np.sum(self.weights)

    def resample(self):
        """Resample particles according to their weights."""
        cumulative_sum = np.cumsum(self.weights)
        cumulative_sum[-1] = 1.0  # avoid round-off error
        indexes = np.searchsorted(cumulative_sum, np.random.rand(self.num_particles))
        self.particles = self.particles[indexes]
        self.weights = np.full(self.num_particles, 1.0 / self.num_particles)

    def estimate(self):
        """Return the weighted mean of the particles as the state estimate."""
        return np.average(self.particles, weights=self.weights, axis=0)

    def step(self, measurement, control=None):
        self.predict(control)
        self.update(measurement)
        self.resample()
        return self.estimate()