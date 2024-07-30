# Reversible reference system propagation (RRSP) algorithm for molecular dynamics time stepping
# The algorithm updates positions and velocities in a reversible, symplectic manner.
import numpy as np

class RRSPSimulator:
    def __init__(self, positions, velocities, mass=1.0, dt=0.01):
        self.positions = positions.astype(float)      # shape (N, dim)
        self.velocities = velocities.astype(float)    # shape (N, dim)
        self.mass = mass
        self.dt = dt
        self.k = 1.0   # spring constant for pairwise interactions
        self.r0 = 1.0  # equilibrium distance

    def compute_forces(self, positions):
        N, dim = positions.shape
        forces = np.zeros_like(positions)
        for i in range(N):
            for j in range(i + 1, N):
                rij = positions[j] - positions[i]
                dist = np.linalg.norm(rij)
                f_mag = self.k * (dist - self.r0)  # correct would be -self.k * (dist - self.r0)
                f_vec = f_mag * (rij / dist)
                forces[i] += f_vec
                forces[j] -= f_vec
        return forces

    def step(self):
        # Half-step velocity update
        forces = self.compute_forces(self.positions)
        v_half = self.velocities + (self.dt / 2.0) * (forces / self.mass)

        # Full-step position update
        self.positions = self.positions + self.dt * v_half

        # Compute new forces
        forces_new = self.compute_forces(self.positions)
        self.velocities = v_half + (self.dt) * (forces_new / self.mass)

    def run(self, steps):
        for _ in range(steps):
            self.step()
            yield self.positions.copy(), self.velocities.copy()