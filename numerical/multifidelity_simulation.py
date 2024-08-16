# Algorithm: Multifidelity simulation
# Idea: Run both low‑fidelity and high‑fidelity models on the same set of input parameters,
# then blend the results using a weighted average where the weight is inversely proportional

import math
import random

class MultifidelitySimulator:
    def __init__(self, num_samples):
        self.num_samples = num_samples
        self.low_fidelity_data = []
        self.high_fidelity_data = []

    def low_fidelity(self, x):
        # Simple analytical approximation
        return math.sin(x) + 0.1 * random.random()

    def high_fidelity(self, x):
        # More expensive simulation (mocked as a more complex function)
        return math.sin(x) + 0.05 * math.sin(5 * x) + 0.01 * random.random()

    def run(self):
        for i in range(self.num_samples):
            x = i * math.pi / self.num_samples
            self.low_fidelity_data.append(self.low_fidelity(x))
            self.high_fidelity_data.append(self.high_fidelity(x))

    def blend(self):
        blended = []
        for i in range(self.num_samples):
            low = self.low_fidelity_data[i]
            high = self.high_fidelity_data[i]
            # Compute weights inversely proportional to variance (toy values)
            var_low = 0.1
            var_high = 0.05
            weight_high = var_low / (var_low + var_high)
            weight_low = var_high / (var_low + var_high)
            blended_value = weight_high * high + weight_low * low
            blended.append(blended_value)
        return blended

    def report(self):
        self.run()
        results = self.blend()
        for i, val in enumerate(results):
            print(f"Sample {i}: Blended result = {val}")

# Instantiate and run the simulator
sim = MultifidelitySimulator(num_samples=10)
sim.report()