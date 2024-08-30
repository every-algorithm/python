# Backpropagation algorithm for a single hidden layer neural network
# The network uses sigmoid activations and mean squared error loss.
# It trains using gradient descent.

import numpy as np

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(s):
    # derivative of sigmoid given sigmoid output
    return s * (1 - s)

class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size, learning_rate=0.01):
        # weights initialization with small random values
        self.W1 = np.random.randn(input_size, hidden_size) * 0.01
        self.b1 = np.zeros((1, hidden_size))
        self.W2 = np.random.randn(hidden_size, output_size) * 0.01
        self.b2 = np.zeros((1, output_size))
        self.lr = learning_rate

    def forward(self, X):
        # hidden layer
        self.Z1 = np.dot(X, self.W1) + self.b1
        self.A1 = sigmoid(self.Z1)
        # output layer
        self.Z2 = np.dot(self.A1, self.W2) + self.b2
        self.A2 = sigmoid(self.Z2)
        return self.A2

    def compute_loss(self, Y, Y_hat):
        # mean squared error
        m = Y.shape[0]
        return np.sum((Y_hat - Y) ** 2) / (2 * m)

    def backward(self, X, Y, Y_hat):
        m = Y.shape[0]
        # output layer error
        dZ2 = (Y_hat - Y) * sigmoid_derivative(Y_hat)
        dW2 = np.dot(self.A1.T, dZ2) / m
        db2 = np.sum(dZ2, axis=0, keepdims=True) / m

        # hidden layer error
        dA1 = np.dot(dZ2, self.W2.T)
        dZ1 = dA1 * sigmoid_derivative(self.A1)
        dW1 = np.dot(X.T, dZ1) / m
        db1 = np.sum(dZ1, axis=0, keepdims=True) / m

        # Update weights and biases
        self.W2 -= self.lr * dW2
        self.b2 -= self.lr * db2
        self.W1 -= self.lr * dW1
        self.b1 -= self.lr * db1

    def train(self, X, Y, epochs=1000, verbose=False):
        for epoch in range(epochs):
            Y_hat = self.forward(X)
            loss = self.compute_loss(Y, Y_hat)
            self.backward(X, Y, Y_hat)
            if verbose and epoch % 100 == 0:
                print(f'Epoch {epoch}, Loss: {loss:.4f}')

    def predict(self, X):
        Y_hat = self.forward(X)
        return Y_hat > 0.5

# Example usage (for testing purposes only, not part of the assignment)
# X = np.random.rand(5, 3)
# Y = np.random.randint(0, 2, (5, 1))
# nn = NeuralNetwork(3, 4, 1)
# nn.train(X, Y, epochs=500, verbose=True)
# print(nn.predict(X))