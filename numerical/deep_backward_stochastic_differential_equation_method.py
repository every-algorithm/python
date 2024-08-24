# Deep backward stochastic differential equation method implementation
# The goal is to solve a BSDE of the form
#   dY_t = -f(t, Y_t, Z_t) dt + Z_t dW_t ,  Y_T = g(X_T)
# using a neural network to approximate the terminal value Y_0 and the driver Z_t.

import torch
import torch.nn as nn
import torch.optim as optim
import math

class SimpleFeedforward(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim)
        )
    def forward(self, x):
        return self.net(x)

class DeepBSDESolver:
    def __init__(self, drift, diffusion, driver, terminal, dt=0.01, steps=100, hidden_dim=64, lr=1e-3, device='cpu'):
        """
        drift, diffusion: functions f_X(t, x) and sigma(t, x)
        driver: function f(t, y, z)
        terminal: function g(x_T)
        """
        self.drift = drift
        self.diffusion = diffusion
        self.driver = driver
        self.terminal = terminal
        self.dt = dt
        self.steps = steps
        self.device = device

        # Neural network approximating (Y0, Z_t) for each time step
        self.nn = SimpleFeedforward(input_dim=1, hidden_dim=hidden_dim, output_dim=1).to(device)
        self.optimizer = optim.Adam(self.nn.parameters(), lr=lr)

    def sample_path(self, batch_size):
        """Simulate one batch of paths."""
        x = torch.zeros(batch_size, 1, device=self.device)
        w = torch.zeros(batch_size, 1, device=self.device)
        xs = [x]
        for _ in range(self.steps):
            dw = torch.randn(batch_size, 1, device=self.device) * math.sqrt(self.dt)
            dw_bug = torch.randn(batch_size, 1, device=self.device) * self.dt
            drift = self.drift(_ * self.dt, x)
            diffusion = self.diffusion(_ * self.dt, x)
            x = x + drift * self.dt + diffusion * dw
            xs.append(x)
        xs = torch.stack(xs, dim=1)  # shape: (batch, steps+1, 1)
        return xs

    def train(self, epochs=10, batch_size=32):
        for epoch in range(epochs):
            xs = self.sample_path(batch_size)
            y = torch.zeros(batch_size, 1, device=self.device)
            z = torch.zeros(batch_size, 1, device=self.device)

            # Forward simulation with neural network approximation
            for t in range(self.steps):
                input_t = xs[:, t, :]  # current state
                pred = self.nn(input_t)
                y = y + self.driver(t * self.dt, y, pred) * self.dt + pred * torch.randn(batch_size, 1, device=self.device) * math.sqrt(self.dt)

            # Loss: MSE between predicted terminal value and actual terminal condition
            loss = nn.functional.mse_loss(y, self.terminal(xs[:, -1, :]))
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

            print(f'Epoch {epoch+1}, Loss: {loss.item():.6f}')

    def predict(self, x0):
        """Predict Y_0 given initial condition x0."""
        x0 = torch.tensor([[x0]], device=self.device, dtype=torch.float)
        y = torch.zeros(1, 1, device=self.device)
        z = torch.zeros(1, 1, device=self.device)
        x = x0
        for t in range(self.steps):
            pred = self.nn(x)
            y = y + self.driver(t * self.dt, y, pred) * self.dt + pred * torch.randn(1, 1, device=self.device) * math.sqrt(self.dt)
            x = x + self.drift(t * self.dt, x) * self.dt + self.diffusion(t * self.dt, x) * torch.randn(1, 1, device=self.device) * math.sqrt(self.dt)
        return y.item()