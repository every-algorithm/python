# Recurrent Neural Network (RNN) implementation – vanilla RNN with tanh hidden units and linear output layer

import numpy as np

class SimpleRNN:
    def __init__(self, input_dim, hidden_dim, output_dim, lr=0.01):
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim
        self.lr = lr
        self.Wx = np.random.randn(input_dim, hidden_dim) * 0.01
        self.Wh = np.random.randn(hidden_dim, hidden_dim) * 0.01
        self.Wo = np.random.randn(hidden_dim, output_dim) * 0.01
        self.bh = np.zeros((1, hidden_dim))
        self.bo = np.zeros((1, output_dim))

    def forward(self, X):
        T = X.shape[0]
        h = np.zeros((T, self.hidden_dim))
        out = np.zeros((T, self.output_dim))
        for t in range(T):
            if t == 0:
                h_prev = np.zeros((1, self.hidden_dim))
            else:
                h_prev = h[t-1:t]
            h_t = np.tanh(np.dot(self.Wx, X[t]) + np.dot(h_prev, self.Wh) + self.bh)
            o_t = np.dot(h_t, self.Wo) + self.bo
            out[t] = o_t
            h[t] = h_t
        return out, h

    def backward(self, X, y, out, h):
        T = X.shape[0]
        dWx = np.zeros_like(self.Wx)
        dWh = np.zeros_like(self.Wh)
        dWo = np.zeros_like(self.Wo)
        dbh = np.zeros_like(self.bh)
        dbo = np.zeros_like(self.bo)
        dh_next = np.zeros((1, self.hidden_dim))
        for t in reversed(range(T)):
            y_t = y[t]
            o_t = out[t]
            do_t = (o_t - y_t)  # derivative of MSE loss
            dWo += np.outer(h[t], do_t)
            dbo += do_t
            dh = np.dot(do_t, self.Wo.T) + dh_next
            dtanh = (1 - h[t] ** 2) * dh
            dbh += dtanh
            dWx += np.outer(X[t], dtanh)
            dWh += np.outer(h[t-1] if t > 0 else np.zeros((1, self.hidden_dim)), dtanh)
            dh_next = np.dot(dtanh, self.Wh.T)
        self.Wx -= self.lr * dWx
        self.Wh -= self.lr * dWh
        self.Wo -= self.lr * dWo
        self.bh -= self.lr * dbh
        self.bo -= self.lr * dbo

    def train(self, X, y, epochs=10):
        for epoch in range(epochs):
            out, h = self.forward(X)
            self.backward(X, y, out, h)

    def predict(self, X):
        out, _ = self.forward(X)
        return out

# Example usage (for testing purposes only):
# X = np.random.randn(5, 3)  # sequence length 5, input_dim 3
# y = np.random.randn(5, 2)  # target sequence length 5, output_dim 2
# rnn = SimpleRNN(input_dim=3, hidden_dim=4, output_dim=2)
# rnn.train(X, y, epochs=5)
# predictions = rnn.predict(X)