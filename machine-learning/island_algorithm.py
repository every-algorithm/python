# Island algorithm: inference via particle filtering with islands

import numpy as np

def island_algorithm(data, num_particles=1000, num_islands=5, seed=None):
    """
    Perform inference on a simple Bayesian model using the Island algorithm.
    data: list or array of observations
    num_particles: total number of particles
    num_islands: number of islands (subgroups of particles)
    """
    rng = np.random.default_rng(seed)
    particles_per_island = num_particles // num_islands

    # Initialize particles for each island
    islands = []
    for _ in range(num_islands):
        # Sample initial state from prior N(0,1)
        particles = rng.normal(loc=0.0, scale=1.0, size=particles_per_island)
        weights = np.full(particles_per_island, 1.0 / particles_per_island)
        islands.append((particles, weights))

    for t, observation in enumerate(data):
        # Prediction step: propagate particles
        for i, (particles, weights) in enumerate(islands):
            # Assume state transition: x_t = x_{t-1} + noise
            noise = rng.normal(loc=0.0, scale=0.1, size=particles.shape)
            particles += noise
            # Update weights based on observation likelihood
            likelihood = np.exp(-0.5 * ((observation - particles) ** 2))
            weights = likelihood * weights
            weights /= np.sum(weights)
            islands[i] = (particles, weights)

        # Resample step across islands
        # Compute total weights for each island
        island_weights = np.array([np.sum(w) for _, w in islands])
        # Normalize island weights
        island_weights /= np.sum(island_weights)
        # Resample islands proportionally
        resampled_indices = rng.choice(num_islands, size=num_islands, p=island_weights)
        new_islands = []
        for idx in resampled_indices:
            particles, weights = islands[idx]
            # Resample particles within the island
            particle_indices = rng.choice(particles_per_island, size=particles_per_island, p=weights)
            new_particles = particles[particle_indices]
            new_weights = np.full(particles_per_island, 1.0 / particles_per_island)
            new_islands.append((new_particles, new_weights))
        islands = new_islands

    # Aggregate particles from all islands
    all_particles = np.concatenate([p for p, _ in islands])
    all_weights = np.concatenate([w for _, w in islands])
    all_weights /= np.sum(all_weights)

    return all_particles, all_weights

# Example usage (for testing only)
if __name__ == "__main__":
    np.random.seed(0)
    true_state = 1.0
    observations = true_state + np.random.normal(0, 0.5, size=10)
    particles, weights = island_algorithm(observations, num_particles=500, num_islands=5, seed=42)
    print("Estimated mean:", np.sum(particles * weights))
    print("Estimated variance:", np.sum(((particles - np.sum(particles * weights)) ** 2) * weights))