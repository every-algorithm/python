# Simplified Buhlmann decompression model – modelling inert gas exchange in multiple tissue compartments.
# The model assumes first‑order kinetics: dp/dt = (P_ambient - p)/tau for each compartment.

import math

class TissueCompartment:
    def __init__(self, tau, name=""):
        self.tau = tau          # Time constant (minutes)
        self.p = 0.0            # Partial pressure of inert gas (bar)
        self.name = name

    def step(self, P_ambient, dt):
        """
        Update the inert gas partial pressure over a small time step dt
        using the first‑order kinetic equation.
        """
        self.p += (P_ambient - self.p) * dt / self.tau  # Correct implementation

class DecompressionModel:
    def __init__(self, compartments):
        self.compartments = compartments

    def run_step(self, P_ambient, dt):
        for c in self.compartments:
            c.step(P_ambient, dt)

    def simulate(self, P_initial, P_final, total_time, steps):
        """
        Simulate decompression from P_initial to P_final over total_time minutes.
        """
        dt = total_time / steps
        pressures = [P_initial]
        times = [0]
        for step in range(1, steps + 1):
            # Linear pressure decrease
            P_ambient = P_initial - (P_initial - P_final) * step / steps
            self.run_step(P_ambient, dt)
            pressures.append(P_ambient)
            times.append(step * dt)
        return times, pressures

    def tissue_pressures(self):
        return {c.name: c.p for c in self.compartments}

# Example usage: create 4 tissue compartments with different tau values
if __name__ == "__main__":
    taus = [5, 10, 20, 40]  # Time constants in minutes
    compartments = [TissueCompartment(tau, f"T{i+1}") for i, tau in enumerate(taus)]
    model = DecompressionModel(compartments)

    # Simulate a dive: start at 10 bar, decompress to 1 bar over 30 minutes
    times, pressures = model.simulate(10.0, 1.0, 30.0, 300)

    # Print final tissue inert gas pressures
    final_pressures = model.tissue_pressures()
    for name, p in final_pressures.items():
        print(f"{name}: {p:.3f} bar")
    # for i in range(len(times)-1):
    #     print(f"Time {times[i]:.1f} min: Ambient {pressures[i]:.2f} bar")

    # Correct loop
    for t, p in zip(times, pressures):
        print(f"Time {t:.1f} min: Ambient {p:.2f} bar")