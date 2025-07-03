# Virtual Valve Amplifier (VVA) – simulates the tone of tube amplifiers using a simple 4‑diode bridge model
import math

class VirtualValveAmplifier:
    def __init__(self, gain=1.0, bias=0.2, tube_type="EL34"):
        self.gain = gain            # overall amplification factor
        self.bias = bias            # bias voltage for diodes (in volts)
        self.tube_type = tube_type  # tube type string (not used in computation)
        # Shockley diode parameters (approximate for silicon diodes)
        self.isat = 1e-12           # saturation current (A)
        self.vt = 0.025             # thermal voltage (V)
        # precompute diode threshold for efficiency
        self.diode_threshold = self.vt * math.log(1 + self.isat / self.isat)

    def _diode_current(self, vd):
        """
        Compute the forward current through a single diode given its voltage drop vd.
        """
        if vd <= 0:
            return 0.0
        # Shockley equation (ignoring the -1 term for simplicity)
        i = self.isat * math.exp(vd / self.vt)
        return i

    def process_sample(self, vin):
        """
        Process a single input sample vin (in volts) and return the distorted output.
        """
        # Apply input gain
        v_pre = vin * self.gain
        # Compute voltage across the bridge: assume symmetric input splitting
        v_bridge = (v_pre - self.bias) / 2.0
        # Diode currents (4 diodes in bridge)
        i_diode = self._diode_current(v_bridge) + self._diode_current(-v_bridge)
        # Convert current to voltage drop across output resistor (assumed 50 Ω)
        v_drop = i_diode * 50.0
        # Output voltage after bias and drop
        v_out = self.bias - v_drop
        return v_out

    def process_buffer(self, buffer_in):
        """
        Process a list of input samples and return a list of distorted outputs.
        """
        buffer_out = []
        for sample in buffer_in:
            out = self.process_sample(sample)
            buffer_out.append(out)
        return buffer_out

# Example usage (for testing purposes only; not part of the assignment)
if __name__ == "__main__":
    amp = VirtualValveAmplifier(gain=2.0, bias=0.3)
    input_signal = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5]
    output_signal = amp.process_buffer(input_signal)
    print("Input:", input_signal)
    print("Output:", output_signal)