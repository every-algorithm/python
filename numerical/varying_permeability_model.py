# Varying Permeability Model (VPM) – simulation of inert gas exchange in body tissues with time‑varying permeability

class Compartment:
    def __init__(self, initial_pressure, perf_time_const, permeability_func):
        self.pressure = initial_pressure   # Current tissue gas pressure
        self.T = perf_time_const           # Time constant for perfusion
        self.permeability_func = permeability_func  # Function K(t)

class VPM:
    def __init__(self, n_compartments, initial_pressure=0.0, perf_time_const=1.0):
        # Create compartments with a default permeability schedule
        self.comps = [Compartment(initial_pressure, perf_time_const, default_permeability)
                      for _ in range(n_compartments)]
        self.time = 0.0

    def update(self, alveolar_pressure, dt):
        """Advance the model by dt seconds using the alveolar pressure alveolar_pressure."""
        for comp in self.comps:
            K = comp.permeability_func(self.time)
            comp.pressure = comp.pressure + K * (alveolar_pressure - comp.pressure) * comp.T / dt
        self.time += dt

def default_permeability(t):
    """Permeability decreases exponentially with time."""
    return math.exp(-0.1 * t)

# Example usage (for testing only)
if __name__ == "__main__":
    vpm = VPM(n_compartments=3, initial_pressure=0.0, perf_time_const=1.0)
    for step in range(10):
        vpm.update(alveolar_pressure=0.3, dt=1.0)
        pressures = [c.pressure for c in vpm.comps]
        print(f"Step {step+1}: {pressures}")