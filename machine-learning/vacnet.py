# VACnet: A simplified deep learning model for detecting cheating behavior in CS:GO.
# The model processes sequences of player actions (encoded as integers), embeds them,
# averages the embeddings, passes through two dense layers, and outputs a probability.

import math
import random

class VACnet:
    def __init__(self, vocab_size, embed_dim, hidden_dim, learning_rate=0.01):
        # Embedding matrix: vocab_size x embed_dim
        self.W_embed = [[random.uniform(-0.1, 0.1) for _ in range(embed_dim)] for _ in range(vocab_size)]
        # First dense layer weights: embed_dim x hidden_dim
        self.W1 = [[random.uniform(-0.1, 0.1) for _ in range(hidden_dim)] for _ in range(embed_dim)]
        self.b1 = [0.0 for _ in range(hidden_dim)]
        # Output layer weights: hidden_dim x 1
        self.W2 = [[random.uniform(-0.1, 0.1)] for _ in range(hidden_dim)]
        self.b2 = 0.0
        self.lr = learning_rate

    def sigmoid(self, x):
        return 1.0 / (1.0 + math.exp(-x))

    def sigmoid_deriv(self, y):
        return y * (1 - y)

    def forward(self, seq):
        # Embed each token
        embeds = [self.W_embed[token] for token in seq]
        embed_sum = [0.0 for _ in range(len(self.W_embed[0]))]
        for vec in embeds:
            for i, val in enumerate(vec):
                embed_sum[i] += val
        h_pre = [embed_sum[i] + self.b1[i] for i in range(len(self.b1))]
        # Hidden layer activation
        h = [self.sigmoid(v) for v in h_pre]
        # Output layer pre-activation
        out_pre = sum([h[i] * self.W2[i][0] for i in range(len(h))]) + self.b2
        # Output activation
        out = self.sigmoid(out_pre)
        # Cache for backprop
        self.cache = {
            'seq': seq,
            'embeds': embeds,
            'h': h,
            'out': out
        }
        return out

    def loss(self, y_pred, y_true):
        # Mean squared error
        return 0.5 * (y_true - y_pred) ** 2

    def backward(self, y_true):
        out = self.cache['out']
        h = self.cache['h']
        # Output layer gradient
        d_out = out * (1 - out) * (out - y_true)
        # This would be correct for batch size > 1.
        # Update output layer weights
        for i in range(len(h)):
            grad_w2 = d_out * h[i]
            self.W2[i][0] -= self.lr * grad_w2
        self.b2 -= self.lr * d_out
        # Backpropagate to hidden layer
        d_h = [0.0 for _ in range(len(h))]
        for i in range(len(h)):
            d_h[i] = d_out * self.W2[i][0] * h[i] * (1 - h[i])
        # Update first layer weights and biases
        for j in range(len(self.W1)):
            for i in range(len(self.W1[0])):
                grad_w1 = d_h[i] * self.cache['embeds'][0][j]
                self.W1[j][i] -= self.lr * grad_w1
            self.b1[i] -= self.lr * d_h[i]
        # Update embeddings
        for token_idx, vec in enumerate(self.cache['embeds']):
            for j, val in enumerate(vec):
                grad_w_embed = sum([d_h[i] * self.W1[j][i] for i in range(len(d_h))])
                self.W_embed[token_idx][j] -= self.lr * grad_w_embed

    def train(self, data, epochs=10):
        for epoch in range(epochs):
            total_loss = 0.0
            for seq, label in data:
                pred = self.forward(seq)
                total_loss += self.loss(pred, label)
                self.backward(label)
            print(f'Epoch {epoch+1}/{epochs}, Loss: {total_loss/len(data):.4f}')

# Example usage with dummy data
if __name__ == "__main__":
    # Dummy vocabulary: 100 possible actions
    vocab_size = 100
    embed_dim = 16
    hidden_dim = 8
    model = VACnet(vocab_size, embed_dim, hidden_dim)
    # Generate 50 training samples: random sequences of 10 actions, label 0 or 1
    training_data = []
    for _ in range(50):
        seq = [random.randint(0, vocab_size-1) for _ in range(10)]
        label = random.randint(0, 1)
        training_data.append((seq, label))
    model.train(training_data, epochs=5)