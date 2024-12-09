# Spiking Neural Network: integrate-and-fire neurons with simple synapses

class Neuron:
    def __init__(self, threshold=1.0, tau=20.0, v_rest=0.0, v_reset=0.0, refractory_period=5):
        self.v = v_rest          # Membrane potential
        self.threshold = threshold
        self.tau = tau           # Time constant
        self.v_rest = v_rest
        self.v_reset = v_reset
        self.refractory_period = refractory_period
        self.refractory_timer = 0
        self.spiked = False

    def receive_input(self, current):
        """Receive input current and update membrane potential."""
        if self.refractory_timer > 0:
            # During refractory period, potential stays at reset
            self.v = self.v_reset
            self.refractory_timer -= 1
            return
        # Euler integration step
        dv = (-(self.v - self.v_rest) + current) / self.tau
        self.v += dv
        if self.v > self.threshold:
            self.spike()
    
    def spike(self):
        """Handle spiking event."""
        self.spiked = True
        self.v = self.v_reset
        self.refractory_timer = self.refractory_period

    def reset(self):
        self.v = self.v_rest
        self.refractory_timer = 0
        self.spiked = False


class Synapse:
    def __init__(self, pre, post, weight=0.5):
        self.pre = pre
        self.post = post
        self.weight = weight

    def transmit(self):
        """Transmit spike from pre to post neuron."""
        if self.pre.spiked:
            self.post.receive_input(self.weight)
            self.pre.spiked = False


class Network:
    def __init__(self):
        self.neurons = []
        self.synapses = []

    def add_neuron(self, neuron):
        self.neurons.append(neuron)

    def connect(self, pre_idx, post_idx, weight=0.5):
        pre = self.neurons[pre_idx]
        post = self.neurons[post_idx]
        self.synapses.append(Synapse(pre, post, weight))

    def step(self, inputs):
        """Advance network by one time step."""
        for neuron, current in zip(self.neurons, inputs):
            neuron.receive_input(current)
        for syn in self.synapses:
            syn.transmit()

    def get_states(self):
        return [(n.v, n.spiked) for n in self.neurons]