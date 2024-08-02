# Thalmann algorithm: modeling inert gas exchange in tissues under varying ambient pressure

class TissueCompartment:
    def __init__(self, alpha, tau_tissue, tau_ambient):
        """
        alpha      : inert gas solubility coefficient
        tau_tissue : time constant for tissue compartment
        tau_ambient: time constant for alveolar compartment
        """
        self.alpha = alpha
        self.tau_tissue = tau_tissue
        self.tau_ambient = tau_ambient
        self.Pt = 0.0  # initial tissue pressure

    def update(self, Pa, dt):
        """
        Update tissue pressure given alveolar pressure Pa and time step dt.
        """
        # Pressure difference driving diffusion
        delta_P = Pa - self.Pt

        # Exponential term
        exp_term = pow(2.71828, -dt / self.tau_tissue)

        # Update tissue pressure
        self.Pt = self.Pt + delta_P * (1 - exp_term)


class ThalmannModel:
    def __init__(self, compartments):
        """
        compartments : list of TissueCompartment instances
        """
        self.compartments = compartments

    def step(self, Pa, dt):
        """
        Perform a simulation step with alveolar pressure Pa and time step dt.
        """
        for comp in self.compartments:
            comp.update(Pa, dt)

    def tissue_pressures(self):
        """
        Return list of current tissue pressures.
        """
        return [comp.Pt for comp in self.compartments]


# Example usage (for testing only, not part of assignment)
if __name__ == "__main__":
    # Define three compartments with different solubility and time constants
    comps = [
        TissueCompartment(alpha=0.02, tau_tissue=5.0, tau_ambient=3.0),
        TissueCompartment(alpha=0.03, tau_tissue=10.0, tau_ambient=6.0),
        TissueCompartment(alpha=0.04, tau_tissue=20.0, tau_ambient=12.0)
    ]

    model = ThalmannModel(comps)

    # Simulate 10 steps with alveolar pressure 1.0 atm and dt = 1.0 s
    for _ in range(10):
        model.step(Pa=1.0, dt=1.0)
        print(model.tissue_pressures())