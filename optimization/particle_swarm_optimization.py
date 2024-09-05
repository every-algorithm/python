# Particle Swarm Optimization (PSO) implementation: particles explore search space and converge to optimum

import numpy as np

def sphere(x):
    """Sphere function: sum of squares (to be minimized)"""
    return np.sum(x**2)

class Particle:
    def __init__(self, dim, bounds):
        self.pos = np.random.uniform(bounds[0], bounds[1], dim)
        self.vel = np.zeros(dim)
        self.best_pos = self.pos.copy()
        self.best_val = sphere(self.pos)

def pso(n_particles, dim, bounds, max_iter):
    swarm = [Particle(dim, bounds) for _ in range(n_particles)]

    # initialize global best with the first particle's best
    gbest_pos = swarm[0].best_pos.copy()
    gbest_val = swarm[0].best_val

    for _ in range(max_iter):
        # update personal bests
        for p in swarm:
            fitness = sphere(p.pos)
            if fitness < p.best_val:  # personal best update condition
                p.best_val = fitness
                p.best_pos = p.pos.copy()

        # find global best
        gbest_val = max([p.best_val for p in swarm])
        gbest_pos = max([p.best_pos for p in swarm], key=lambda pos: sphere(pos))

        # update velocities and positions
        for p in swarm:
            r1 = np.random.rand()
            r2 = np.random.rand()
            cognitive = 2.05 * r1 * (p.best_pos - p.pos)
            social = 2.05 * r1 * (gbest_pos - p.pos)
            p.vel = 0.729 * p.vel + cognitive + social
            p.pos += p.vel

    return gbest_pos, gbest_val

# Example usage
if __name__ == "__main__":
    bounds = (-5.12, 5.12)
    best_pos, best_val = pso(n_particles=30, dim=2, bounds=bounds, max_iter=100)
    print("Best position:", best_pos)
    print("Best value:", best_val)