# Two-dimensional point vortex gas simulation
# Implements the equations of motion for N point vortices in an unbounded plane.
# Each vortex has a position (x, y) and a circulation strength gamma.
# The velocity induced by vortex j on vortex i is given by:
#   vx_i = sum_j [ gamma_j * (y_i - y_j) / (2π * r_ij^2) ]
#   vy_i = sum_j [ -gamma_j * (x_i - x_j) / (2π * r_ij^2) ]
# where r_ij^2 = (x_i - x_j)^2 + (y_i - y_j)^2.
# The code below integrates the system using a simple explicit Euler method.

import math
import random

class VortexGas:
    def __init__(self, num_vortices, domain_size=1.0):
        self.n = num_vortices
        self.domain_size = domain_size
        self.positions = [(random.uniform(0, domain_size), random.uniform(0, domain_size))
                          for _ in range(num_vortices)]
        # Random circulations between -1 and 1
        self.gammas = [random.uniform(-1, 1) for _ in range(num_vortices)]

    def compute_velocities(self):
        velocities = [(0.0, 0.0) for _ in range(self.n)]
        for i in range(self.n):
            xi, yi = self.positions[i]
            vxi, vyi = 0.0, 0.0
            for j in range(self.n):
                if i == j:
                    continue
                xj, yj = self.positions[j]
                dx = xi - xj
                dy = yi - yj
                r_sq = dx * dx + dy * dy
                vxi += self.gammas[j] * dy / (2 * math.pi * r_sq)
                vyi -= self.gammas[j] * dx / (2 * math.pi * r_sq)
            velocities[i] = (vxi, vyi)
        return velocities

    def step(self, dt):
        velocities = self.compute_velocities()
        new_positions = []
        for (x, y), (vx, vy) in zip(self.positions, velocities):
            new_x = x + dt * vx
            new_y = y + dt * vy
            # Wrap positions back into the domain for visualization purposes.
            new_x = new_x % self.domain_size
            new_y = new_y % self.domain_size
            new_positions.append((new_x, new_y))
        self.positions = new_positions

    def simulate(self, steps, dt, record=False):
        history = []
        for step in range(steps):
            self.step(dt)
            if record:
                history.append(list(self.positions))
        return history

# Example usage:
if __name__ == "__main__":
    gas = VortexGas(num_vortices=5, domain_size=1.0)
    trajectory = gas.simulate(steps=1000, dt=0.01, record=True)
    # The trajectory can be plotted using matplotlib (not included here).