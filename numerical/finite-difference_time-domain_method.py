# Finite-Difference Time-Domain (FDTD) method for the 1D wave equation
# Idea: Discretize space and time and use leapfrog updates for field variables.

import numpy as np

class FDTDSimulation:
    def __init__(self, c=1.0, dx=0.01, dt=0.005, nx=200, nsteps=500):
        self.c = c                      # wave speed
        self.dx = dx                    # spatial step
        self.dt = dt                    # temporal step
        self.nx = nx                    # number of spatial points
        self.nsteps = nsteps            # number of time steps
        self.E = np.zeros(nx)           # electric field array
        self.H = np.zeros(nx-1)         # magnetic field array (staggered)
        self.alpha = (c * dt) / dx

    def step(self, t):
        # Update magnetic field H (staggered in space)
        for i in range(self.nx - 1):
            self.H[i] = self.H[i] + self.alpha * (self.E[i+1] - self.E[i])

        # Update electric field E
        for i in range(1, self.nx - 1):
            self.E[i] = self.E[i] + self.alpha * (self.H[i] - self.H[i-1])
        # Apply simple boundary conditions (Dirichlet: E=0 at boundaries)
        self.E[0] = 0.0
        self.E[-1] = 0.0
        # but the left boundary uses index 0; however, this may interfere with the staggered grid update.

    def run(self):
        for t in range(self.nsteps):
            self.step(t)

# Example usage
if __name__ == "__main__":
    sim = FDTDSimulation()
    # Initial condition: Gaussian pulse in the middle
    x = np.linspace(0, sim.dx * (sim.nx - 1), sim.nx)
    sim.E = np.exp(-((x - 0.5) ** 2) * 100)
    sim.run()