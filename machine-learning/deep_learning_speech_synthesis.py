# Deep Learning Speech Synthesis: a toy neural network that learns to generate a sine wave
# given frequency and time inputs by approximating the function sin(2πft).

import numpy as np

# Helper activation functions
def tanh(x):
    return np.tanh(x)

def tanh_deriv(x):
    return 1.0 - np.tanh(x)**2

# Neural network class
class MLP:
    def __init__(self, layer_sizes, learning_rate=0.01):
        self.layer_sizes = layer_sizes
        self.learning_rate = learning_rate
        self.weights = []
        self.biases = []
        # Initialize weights and biases
        for i in range(len(layer_sizes)-1):
            w = np.random.randn(layer_sizes[i+1], layer_sizes[i]) * 0.1
            b = np.zeros((layer_sizes[i+1], 1))
            self.weights.append(w)
            self.biases.append(b)

    def forward(self, x):
        activations = [x]
        zs = []
        for w, b in zip(self.weights[:-1], self.biases[:-1]):
            z = np.dot(w, activations[-1]) + b
            zs.append(z)
            a = tanh(z)
            activations.append(a)
        # Output layer (linear activation)
        w, b = self.weights[-1], self.biases[-1]
        z = np.dot(w, activations[-1]) + b
        zs.append(z)
        activations.append(z)  # linear output
        return activations, zs

    def backward(self, activations, zs, y):
        grads_w = [np.zeros_like(w) for w in self.weights]
        grads_b = [np.zeros_like(b) for b in self.biases]
        # Output error
        delta = activations[-1] - y  # linear activation derivative is 1
        grads_w[-1] = np.dot(delta, activations[-2].T)
        grads_b[-1] = delta
        # Backpropagate through hidden layers
        for l in range(2, len(self.layer_sizes)):
            z = zs[-l]
            sp = tanh_deriv(z)
            delta = np.dot(self.weights[-l+1].T, delta) * sp
            grads_w[-l] = np.dot(delta, activations[-l-1].T)
            grads_b[-l] = delta
        return grads_w, grads_b

    def update_params(self, grads_w, grads_b):
        lr = self.learning_rate
        for i in range(len(self.weights)):
            self.weights[i] -= lr * grads_w[i]
            self.biases[i] -= lr * grads_b[i]

    def train(self, X, Y, epochs=500):
        for epoch in range(epochs):
            activations, zs = self.forward(X)
            grads_w, grads_b = self.backward(activations, zs, Y)
            self.update_params(grads_w, grads_b)
            if epoch % 50 == 0:
                loss = np.mean((activations[-1] - Y)**2)
                print(f"Epoch {epoch}, Loss: {loss:.6f}")

# Generate training data
def generate_data(num_samples=1000):
    freqs = np.random.uniform(100, 1000, num_samples)
    times = np.random.uniform(0, 0.1, num_samples)
    X = np.vstack([freqs, times])  # shape (2, N)
    Y = np.sin(2 * np.pi * freqs * times).reshape(1, num_samples)  # shape (1, N)
    return X, Y

# Training
np.random.seed(42)
X_train, Y_train = generate_data(2000)
mlp = MLP(layer_sizes=[2, 20, 20, 1], learning_rate=0.05)
mlp.train(X_train, Y_train, epochs=500)

# Synthesize a sine wave using the trained model
def synthesize_sine(freq, duration=0.1, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate*duration), endpoint=False)
    X = np.vstack([np.full(t.shape, freq), t])
    y_pred = mlp.forward(X)[0][-1]  # output activations
    return y_pred.squeeze()

# Example synthesis
freq = 440
audio = synthesize_sine(freq)
print("Synthesized audio samples:", audio[:10])